import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
"""
testing
async def get_media():
    session = await MediaManager.request_async()
    current_session = session.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()
        #datos de la cancion
        print(f"Nombre: {info.artist}  Cancion - {info.title}")

        #datos del programa que esta reproduciendo la cancion
        print(current_session.source_app_user_model_id)


        timeline_properties = current_session.get_timeline_properties()
        #TODO: FUNCION PARA OBTENER EL CURRENT TIME DE LA CANCION
        print(f"st{timeline_properties.start_time} et{timeline_properties.end_time}")
        #PONER EL BOTON DE PAUSA
        #PAUSAR
        #current_session.try_pause_async()
        #RESUMIR
        #current_session.try_play_async()
        #SIGUIENTE ROLA
        #current_session.try_skip_next_async()
        #ANTERIOR ROLA
        #current_session.try_skip_previous_async()
    else:
        #AQUI DEBERIA DE PONER EL BOTON DE PLAY
        print("No media playing")
"""
async def get_session():
    session = await MediaManager.request_async()
    current_session = session.get_current_session()
    if current_session:
        return current_session
    else:
        return None

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
        info = await session.try_get_media_properties_async()
        timeline = session.get_timeline_properties()
        title = info.title
        artist = info.artist
        source = session.source_app_user_model_id
        st = timeline.start_time
        et = timeline.end_time
        data = {title, artist, source,st,et}
        return data
    else:
        return None
    
#TODO: FUNCION PARA OBTENER EL CURRENT TIME DE LA CANCION