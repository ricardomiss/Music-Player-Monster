import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader, Buffer, InputStreamOptions
import os
import json
import datetime
from PyQt5.QtCore import pyqtSignal, QObject

class MediaSignals(QObject):
    media_changed = pyqtSignal(object)
    playback_changed = pyqtSignal(object)

media_signals = MediaSignals()

current_session = None

async def request_async():
    session = await MediaManager.request_async()
    return session

async def get_session():
    global current_session
    session = await MediaManager.request_async()
    current_session = session.get_current_session()
    if current_session:
        return current_session
    else:
        return False

async def control_media(estado):
    session = await get_session()
    if session:
        if estado == 1:
            session.try_toggle_play_pause_async()
        elif estado == 2:
            session.try_skip_next_async()
        elif estado == 3:
            session.try_skip_previous_async()
        else:
            return None
    else:
        return None

async def info_media(current_session, event):
    info = await current_session.try_get_media_properties_async()
    timeline = current_session.get_timeline_properties()
    if not info.title and not info.artist:
        thumbnailname = ''
    else:
        thumbnailname = await get_thumbnail(info.thumbnail)
    data = [info.title, info.artist, info.thumbnail, current_session.source_app_user_model_id[:-4], timeline.start_time, timeline.end_time, thumbnailname]
    await save_data(data)
    return data

async def get_thumbnail(thumbnail):
    if not thumbnail:
        return None
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    buffer = Buffer(5000000)
    readable_stream = await thumbnail.open_read_async()
    await readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

    buffer_reader = DataReader.from_buffer(buffer)
    byte_buffer = buffer_reader.read_buffer(buffer.length)
    buffer_reader.detach_buffer()
    if not os.path.exists("history"):
        os.makedirs("history")
    
    with open(f"history/{date}.png", "wb") as f:
        f.write(byte_buffer)
    return f"{date}.png"
        

async def save_data(data):
    if not data[0] and not data[1] and not data[6]:
        return None
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = {
        "title": data[0],
        "artist": data[1],
        "thumbnail": data[6],
        "source": data[3],
        "start_time": str(data[4]),
        "end_time": str(data[5]),
        "date": timestamp
        }
    try:
        if not os.path.exists("history"):
            os.makedirs("history")
        if not os.path.exists("history/data.json"):
            with open("history/data.json", "w", encoding="utf-8") as f:
                f.write('{"history": []}')

        with open("history/data.json", "r+", encoding="utf-8") as f:
            f.seek(0)
            data = json.load(f)
            data["history"].append(json_data)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()
    except Exception as e:
        print(e)

def on_media_properties_changed(sender, e):
    playback_info = sender.get_playback_info()
    if playback_info.playback_status == 0 or playback_info.playback_status == 2:
        return None
    loop = asyncio.new_event_loop()
    datos = loop.run_until_complete(info_media(sender, e))
    media_signals.media_changed.emit(datos)
    loop.close()


def on_current_session_changed(sender, e):
    global current_session
    local_current_session = sender.get_current_session()

    if current_session == None:
        print("primera vez")
        loop = asyncio.new_event_loop()
        loop.run_until_complete(callback())
        loop.close()
        return
    
    if local_current_session != None and (local_current_session.source_app_user_model_id != current_session.source_app_user_model_id):
        print("cambio de sesion")
        print(f"Session changed from: {current_session.source_app_user_model_id} to: {local_current_session.source_app_user_model_id}")
        current_session = local_current_session
        current_session.add_playback_info_changed(on_playback_properties_changed)
        #TODO: FIX THIS
        #current_session.remove_media_properties_changed(on_current_session_changed)
        current_session.add_media_properties_changed(on_media_properties_changed)
        loop = asyncio.new_event_loop()
        datos = loop.run_until_complete(info_media(current_session, None))
        loop.close()
        media_signals.media_changed.emit(datos)
        return

def on_playback_properties_changed(sender, e):
    playback_info = sender.get_playback_info()
    datos = playback_info.playback_status
    media_signals.playback_changed.emit(datos)


#CALLBACK TO OBTAIN SONG INFORMATION AND ITS PLAYBACK STATUS
async def callback():
    session = await request_async()
    current_session = await get_session()
    if current_session:
        datos = await info_media(current_session, None)
        media_signals.media_changed.emit(datos)
        on_playback_properties_changed(current_session, None)
        current_session.add_media_properties_changed(on_media_properties_changed)
        current_session.add_playback_info_changed(on_playback_properties_changed)
        session.add_current_session_changed(on_current_session_changed)
    else:
        session.add_current_session_changed(on_current_session_changed)
    while True:
        await asyncio.sleep(1)

#TODO: FUNCION PARA OBTENER EL CURRENT TIME DE LA CANCION