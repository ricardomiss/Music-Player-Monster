import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader, Buffer, InputStreamOptions
import os
import json
import datetime

async def get_session():
    session = await MediaManager.request_async()
    current_session = session.get_current_session()
    if current_session:
        return current_session
    else:
        #TODO PONER EL BOTON DE PLAY
        return False

async def control_media(estado):
    session = await get_session()
    if session:
        if estado == "play":
            session.try_play_async()
        elif estado == "pause":
            session.try_pause_async()
        elif estado == "next":
            session.try_skip_next_async()
        elif estado == "previous":
            session.try_skip_previous_async()
        else:
            return None
    else:
        return None
    
async def get_media():
    session = await get_session()
    if session:
        data = await info_media(session, None)
        await save_data(data)
        return data
    else:
        return False

async def info_media(current_session, event):
    info = await current_session.try_get_media_properties_async()
    timeline = current_session.get_timeline_properties()
    thumbnailname = await get_thumbnail(info.thumbnail)
    data = [info.title, info.artist, info.thumbnail, current_session.source_app_user_model_id, timeline.start_time, timeline.end_time, thumbnailname]
    return data

async def get_thumbnail(thumbnail):
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
    loop = asyncio.new_event_loop()
    datos = loop.run_until_complete(info_media(sender, e))
    print(datos)

async def callback():
    session = await get_session()
    if session:
        session.add_media_properties_changed(on_media_properties_changed)
    while True:
        pass
        
#TODO: FUNCION PARA OBTENER EL CURRENT TIME DE LA CANCION