import pdb
from flask import request, jsonify
from app.prex_command_detection import detect_command
from app.prex_utils import *
from app.prex_commands import *
from app.prex_config import MODEL, client, prex_story

# Definir la función de la ruta ask_prex
# Definir punto para debug - pdb.set_trace()  # debug n
# Puedes utilizar los siguientes comandos para depurar:
# * `n`: Sigue ejecutando el código hasta la siguiente línea.
# * `s`: Sigue ejecutando el código hasta la siguiente función.
# * `r`: Continúa ejecutando el código desde el punto de ruptura.
# * `c`: Continúa ejecutando el código sin detenerse en puntos de ruptura.
# * `p variable`: Muestra el valor de una variable.
# * `q`: Sale del modo depuración.


def register_prex_routes(app):
    @app.route('/ask_prex', methods=['POST'])
    def ask_prex():

        try:
            data = request.get_json()
            question = data.get('question')
            if not question:
                app.logger.warning('No question provided in request')
                return jsonify({'error': 'No question provided'}), 400

            detected_command = detect_command(question)
            responses = []

            if "ver la ubicación del coche" in detected_command.lower() or "donde estás" in question.lower():
                location_data = get_car_location()
                address = location_data.get("address", "Ubicación desconocida")
                responses.append(
                    f"La ubicación actual del coche es: {address}")

            if "ver batería" in detected_command.lower() or "cuánta batería queda" in question.lower():
                battery_data = get_battery_percentage()
                percentage = battery_data.get("battery_level", "Desconocido")
                responses.append(
                    f"El porcentaje actual de la batería es: {percentage}%")

            if "ver kilómetros restantes" in detected_command.lower() or "alcance de la batería" in question.lower():
                range_data = get_battery_range()
                range_km = range_data.get("battery_range", "Desconocido")
                responses.append(
                    f"El alcance actual de la batería es: {range_km} km")

            if "qué hora es" in detected_command.lower() or "ver hora local" in detected_command.lower() or "hora local" in question.lower():
                location_data = get_car_location()
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")
                timezone = get_timezone_by_location(latitude, longitude)
                if timezone:
                    current_time = get_current_time(timezone)
                    if current_time:
                        responses.append(f"Son las: {current_time}")
                    else:
                        responses.append("No se pudo obtener la hora actual.")
                else:
                    responses.append("No se pudo obtener la zona horaria.")

            if "buscar" in detected_command.lower():
                location_data = get_car_location()
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")
                keyword = detected_command.split("buscar", 1)[1].strip()
                places = find_nearby_places(latitude, longitude, keyword)
                responses.append(f"Lugares cercanos para {
                                 keyword}: \n" + "\n".join(places))

            if "iniciar recarga" in detected_command.lower():
                start_response = start_charging()
                responses.append("Iniciando la recarga del coche." if start_response.get(
                    "response", {}).get("result") else "No se pudo iniciar la recarga del coche.")

            if "parar recarga" in detected_command.lower():
                stop_response = stop_charging()
                responses.append("Parando la recarga del coche." if stop_response.get(
                    "response", {}).get("result") else "No se pudo parar la recarga del coche.")

            if "abrir coche" in detected_command.lower():
                unlock_response = unlock_car()
                responses.append("Abriendo el coche." if unlock_response.get(
                    "response", {}).get("result") else "No se pudo abrir el coche.")

            if "cerrar coche" in detected_command.lower():
                lock_response = lock_car()
                responses.append("Cerrando el coche." if lock_response.get(
                    "response", {}).get("result") else "No se pudo cerrar el coche.")

            if "abrir puerto de recarga" in detected_command.lower():
                open_port_response = open_charge_port()
                responses.append("Abriendo el puerto de recarga." if open_port_response.get(
                    "result") else "No se pudo abrir el puerto de recarga.")

            if "abrir maletero" in detected_command.lower():
                trunk_response = activate_rear_trunk()
                responses.append("Abriendo el maletero trasero." if trunk_response.get(
                    "result") else "No se pudo abrir el maletero trasero.")
            elif "cerrar maletero" in detected_command.lower():
                trunk_response = activate_rear_trunk()
                responses.append("Cerrando el maletero trasero." if trunk_response.get(
                    "result") else "No se pudo cerrar el maletero trasero.")

            if "destellar luces" in detected_command.lower():
                flash_response = flash_lights()
                responses.append("Destellando las luces." if flash_response.get(
                    "result") else "No se pudo destellar las luces.")

            if "tocar bocina" in detected_command.lower() or "pita" in detected_command.lower():
                honk_response = honk_horn()
                responses.append("Tocando la bocina." if honk_response.get(
                    "result") else "No se pudo tocar la bocina.")

            if "ver el tiempo" in detected_command.lower() or "qué tiempo hace" in question.lower():
                weather_data = get_weather()
                temperature = weather_data.get("temperature", "Desconocido")
                condition = weather_data.get("condition", "Desconocido")
                responses.append(f"La temperatura actual es de {
                                 temperature}°C y las condiciones son {condition}.")

            if "encender clima" in detected_command.lower() or "activar clima" in question.lower():
                start_response = start_climate()
                responses.append("Encendiendo el clima." if start_response.get(
                    "result") else "No se pudo encender el clima.")

            if "apagar clima" in detected_command.lower() or "detener clima" in question.lower():
                stop_response = stop_climate()
                responses.append("Apagando el clima." if stop_response.get(
                    "result") else "No se pudo apagar el clima.")

            if "poner temperatura" in detected_command.lower():
                try:
                    driver_temp = float(detected_command.split("a")[
                                        1].strip().split()[0])
                    passenger_temp = driver_temp
                    temp_response = set_temperatures(
                        driver_temp, passenger_temp)
                    responses.append(f"Configurando la temperatura a {driver_temp}°C." if temp_response.get(
                        "result") else "No se pudo configurar la temperatura.")
                except (IndexError, ValueError):
                    responses.append(
                        "No se pudo entender la temperatura especificada.")

            if responses:
             #               pdb.set_trace()
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": prex_story},
                        {"role": "user", "content": question},
                        {"role": "user", "content": " ".join(responses)}
                    ]
                )
                answer = completion.choices[0].message.content.strip()
                audio_filename = generate_audio_response(answer, question)
                return jsonify({'answer': answer, 'audio_url': f'audio/temp/{audio_filename}'})

            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": prex_story},
                    {"role": "user", "content": question}
                ]
            )
            answer = completion.choices[0].message.content.strip()
            audio_filename = generate_audio_response(answer, question)
            return jsonify({'answer': answer, 'audio_url': f'audio/temp/{audio_filename}'})
        except Exception as e:
            app.logger.error('Error in /ask_prex endpoint: %s', e)
            return jsonify({'error': str(e)}), 500

    @app.route('/comando', methods=['POST'])
    def ejecutar_comando():
        try:
            data = request.get_json()
            comando = data.get("comando", "")
            if not comando:
                app.logger.warning('No command provided in request')
                return jsonify({'error': 'No command provided'}), 400

            detected_command = detect_command(comando)
            responses = []

            if "tocar bocina" in detected_command.lower() or "pita" in detected_command.lower():
                honk_response = honk_horn()
                responses.append("Tocando la bocina." if honk_response.get(
                    "result") else "No se pudo tocar la bocina.")

            if "ver la ubicación del coche" in detected_command.lower() or "donde estás" in comando.lower():
                location_data = get_car_location()
                address = location_data.get("address", "Ubicación desconocida")
                responses.append(
                    f"La ubicación actual del coche es: {address}")

            if "ver el porcentaje de batería" in detected_command.lower() or "cuánta batería tienes" in comando.lower() or "batería restante" in comando.lower():
                battery_data = get_battery_percentage()
                percentage = battery_data.get("battery_level", "Desconocido")
                responses.append(
                    f"El porcentaje actual de la batería es: {percentage}%")

            if "ver los kilómetros restantes" in detected_command.lower() or "alcance de la batería" in comando.lower():
                range_data = get_battery_range()
                range_km = range_data.get("battery_range", "Desconocido")
                responses.append(
                    f"El alcance actual de la batería es: {range_km} km")

            if "qué hora es" in detected_command.lower() or "hora local" in comando.lower():
                location_data = get_car_location()
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")
                timezone = get_timezone_by_location(latitude, longitude)
                if timezone:
                    current_time = get_current_time(timezone)
                    if current_time:
                        responses.append(
                            f"La hora local actual es: {current_time}")
                    else:
                        responses.append("No se pudo obtener la hora actual.")
                else:
                    responses.append("No se pudo obtener la zona horaria.")

            if "buscar" in detected_command.lower():
                location_data = get_car_location()
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")
                keyword = detected_command.split("buscar", 1)[1].strip()
                places = find_nearby_places(latitude, longitude, keyword)
                responses.append(f"Lugares cercanos para {
                                 keyword}: \n" + "\n".join(places))

            if "iniciar recarga" in detected_command.lower():
                start_response = start_charging()
                responses.append("Iniciando la recarga del coche." if start_response.get(
                    "response", {}).get("result") else "No se pudo iniciar la recarga del coche.")

            if "parar recarga" in detected_command.lower():
                stop_response = stop_charging()
                responses.append("Parando la recarga del coche." if stop_response.get(
                    "response", {}).get("result") else "No se pudo parar la recarga del coche.")

            if "abrir coche" in detected_command.lower():
                unlock_response = unlock_car()
                responses.append("Abriendo el coche." if unlock_response.get(
                    "response", {}).get("result") else "No se pudo abrir el coche.")

            if "cerrar coche" in detected_command.lower():
                lock_response = lock_car()
                responses.append("Cerrando el coche." if lock_response.get(
                    "response", {}).get("result") else "No se pudo cerrar el coche.")

            if "abrir puerto de recarga" in detected_command.lower():
                open_port_response = open_charge_port()
                responses.append("Abriendo el puerto de recarga." if open_port_response.get(
                    "result") else "No se pudo abrir el puerto de recarga.")

            if "abrir maletero" in detected_command.lower():
                trunk_response = activate_rear_trunk()
                responses.append("Abriendo el maletero trasero." if trunk_response.get(
                    "result") else "No se pudo abrir el maletero trasero.")
            elif "cerrar maletero" in detected_command.lower():
                trunk_response = activate_rear_trunk()
                responses.append("Cerrando el maletero trasero." if trunk_response.get(
                    "result") else "No se pudo cerrar el maletero trasero.")

            if "destellar luces" in detected_command.lower():
                flash_response = flash_lights()
                responses.append("Destellando las luces." if flash_response.get(
                    "result") else "No se pudo destellar las luces.")

            if "encender clima" in detected_command.lower() or "activar clima" in comando.lower():
                start_response = start_climate()
                responses.append("Encendiendo el clima." if start_response.get(
                    "result") else "No se pudo encender el clima.")

            if "apagar clima" in detected_command.lower() or "detener clima" in comando.lower():
                stop_response = stop_climate()
                responses.append("Apagando el clima." if stop_response.get(
                    "result") else "No se pudo apagar el clima.")

            if "poner temperatura" in detected_command.lower():
                try:
                    driver_temp = float(detected_command.split("a")[
                                        1].strip().split()[0])
                    passenger_temp = driver_temp
                    temp_response = set_temperatures(
                        driver_temp, passenger_temp)
                    responses.append(f"Configurando la temperatura a {driver_temp}°C." if temp_response.get(
                        "result") else "No se pudo configurar la temperatura.")
                except (IndexError, ValueError):
                    responses.append(
                        "No se pudo entender la temperatura especificada.")

            if responses:
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": prex_story},
                        {"role": "user", "content": comando},
                        {"role": "user", "content": " ".join(responses)}
                    ]
                )
                respuesta = completion.choices[0].message.content.strip()
                app.logger.info(
                    'Responses generated successfully: %s', responses)
                return jsonify({'respuesta': respuesta})

            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": prex_story},
                    {"role": "user", "content": comando}
                ]
            )
            respuesta = completion.choices[0].message.content.strip()
            return jsonify({'respuesta': respuesta})
        except Exception as e:
            app.logger.error('Error in /comando endpoint: %s', e)
            return jsonify({'error': str(e)}), 500
