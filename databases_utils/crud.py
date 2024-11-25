__version__='1.3.7'
__authors__=['Ioannis Tsakmakis']
__date_created__='2023-10-20'
__last_updated__='2024-10-22'

# from databases_utils import schemas, models
from databases_utils import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import text, select, update
from .aws_utils import KeyManagementService
from .decorators import session_handler_add_delete_update, session_handler_query, validate_int, validate_str, validate_float

class User:

    @staticmethod
    @session_handler_add_delete_update
    def add(user: schemas.UsersTableCreate, db: Session = None):
        new_user = models.Users(aws_user_name=user.aws_user_name, email=user.email, account_type=user.account_type, subscription_expires_in=user.subscription_expires_in)
        db.add(new_user)

    @staticmethod
    @validate_str('aws_user_name')
    @session_handler_query
    def get_by_name(name: str, db: Session = None):
        return db.execute(select(models.Users).filter_by(aws_user_name=name)).one_or_none()

    @staticmethod
    @validate_int('user_id')
    @session_handler_query
    def get_by_id(user_id: int, db: Session = None):
        return db.execute(select(models.Users).filter_by(user_id=user_id)).one_or_none()

    @staticmethod
    @validate_str('email')
    @session_handler_query
    def get_by_email(email: str, db: Session = None):
        return db.execute(select(models.Users).filter_by(email=email)).one_or_none()

    @staticmethod
    @validate_str('aws_user_name')
    @session_handler_add_delete_update
    def delete_by_name(name: str, db: Session = None):
            result = db.execute(select(models.Users).filter_by(aws_user_name=name)).one_or_none()
            if result is not None:
                db.delete(result.Users)
            else:
                return {"message": "Not Found", "errors": ["The provided name does not exist in the users table"]}, 404

class IoTDevices:

    @staticmethod
    @session_handler_add_delete_update
    def add(IoT_device: schemas.IoTDevicesCreate, db: Session = None):
        new_device = models.IoTDevices(manufacturer_id=IoT_device.manufacturer_id, access=IoT_device.access, icon_type=IoT_device.icon_type)
        db.add(new_device)

    @staticmethod
    @validate_int('device_id')
    @session_handler_query
    def get_by_id(device_id: int, db: Session = None):
        return db.execute(select(models.IoTDevices).filter_by(device_id = device_id)).one_or_none()

    @staticmethod
    @session_handler_query
    @validate_str('manufacturer')
    def get_by_manufacturer(manufacturer: str, db: Session = None):
        return db.execute(select(models.IoTDevices).filter_by(manufacturer = manufacturer)).all()

    @staticmethod
    @validate_int('user_id')
    @session_handler_query
    def get_by_access(user_id: int, db: Session = None):
        return db.execute(select(models.IoTDevices).filter(text("JSON_CONTAINS(JSON_UNQUOTE(JSON_EXTRACT(access, '$.users')), CAST(:user AS JSON), '$')").params(user=user_id))).all() 
    
    @staticmethod
    @validate_int('station_id','user_id')
    @session_handler_add_delete_update
    def add_user_to_station(device_id: int, user_id: int, db: Session = None):
        access=db.execute(select(models.IoTDevices).filter_by(device_id=device_id)).one_or_none()
        if user_id not in access[0].access['users']:
            access[0].access['users'].append(user_id)

    @staticmethod
    @validate_int('station_id','user_id')
    @session_handler_add_delete_update
    def delete_user_from_station(device_id: int, user_id: int, db: Session = None):
        access=db.execute(select(models.IoTDevices).filter_by(device_id=device_id)).one_or_none()
        if access.IoTdevices:
            if user_id not in access[0].access['users']:
                access[0].access['users'].remove(user_id)

    @staticmethod
    @validate_int('device_id')
    @session_handler_add_delete_update
    def delete_by_device_id(device_id: int, db: Session = None):
        result = db.execute(select(models.IoTDevices).filter_by(device_id = device_id)).one_or_none()
        if result is not None:
            db.delete(result.IoTdevices)
        else:
            return {"message": "Not Found", "errors": ["The provided device_id does not exist in the stations table"]}, 404

class Manufacturers:

    @staticmethod
    @session_handler_add_delete_update
    def add(manufacturer: schemas.ManufacturersCreate, db: Session = None):
        new_manufacturer = models.Manufacturers(name=manufacturer.name, api_url=manufacturer.api_url, api_version=manufacturer.api_version,
                                                templates=manufacturer.templates)
        db.add(new_manufacturer)

    @staticmethod
    @validate_str('name')
    @session_handler_query
    def get_by_name(name: str, db: Session = None):
        return db.execute(select(models.Manufacturers).filter_by(name=name)).one_or_none()

class ADCONServer:

    @staticmethod
    @session_handler_add_delete_update
    def add(server: schemas.ADCONServerCreate, db: Session = None):
        new_server = models.ADCONServer(server_id=server.server_id, source_id=server.source_id, template=server.template, name=server.name, main_class=server.main_class,
                                        sub_class=server.sub_class, type=server.type, version=server.version, serial=server.serial, code=server.code, time_zone=server.time_zone,
                                        last_update=server.last_update, slot_interval=server.slot_interval, get_data_max_slots=server.get_data_max_slots, get_data_max_nodes=server.get_data_max_nodes)
        db.add(new_server)

    @staticmethod
    @validate_int('server_id')
    @session_handler_query
    def get_by_id(server_id: str, db: Session = None):
        return db.execute(select(models.ADCONServer).filter_by(server_id = server_id)).one_or_none()

    @staticmethod
    @validate_str('source_id')
    @session_handler_query
    def get_by_code(source_id: str, db: Session = None):
        return db.execute(select(models.ADCONServer).filter_by(source_id= source_id)).one_or_none()

    @staticmethod
    @validate_str('serial')
    @session_handler_query
    def get_by_serial(serial: str, db: Session = None):
        return db.execute(select(models.ADCONServer).filter_by(serial=serial)).one_or_none()
    
    @staticmethod
    @validate_int('server_id')
    @validate_float('new_datetime')
    @session_handler_add_delete_update
    def update_last_update(server_id: int, new_datetime: float, db: Session = None):
        db.execute(update(models.ADCONServer).where(models.ADCONServer.server_id==server_id).values(last_update=new_datetime))

class ADCONArea:

    @staticmethod
    @session_handler_add_delete_update
    def add(area: schemas.ADCONAreaCreate, db: Session = None):
        new_are = models.ADCONArea(server_id=area.server_id, source_id=area.source_id, name=area.name, template=area.template, main_class=area.main_class, sub_class=area.sub_class)
        db.add(new_are)

    @staticmethod
    @validate_int('area_id')
    @session_handler_query
    def get_by_area_id(area_id: int, db: Session = None):
        return db.execute(select(models.ADCONArea).filter_by(area_id=area_id)).one_or_none()

    @staticmethod
    @validate_str('source_id')
    @session_handler_query
    def get_by_source_id(source_id: str, db: Session = None):
        return db.execute(select(models.ADCONArea).filter_by(source_id=source_id)).one_or_none()
    
    @staticmethod
    @validate_str('source_id')
    @session_handler_add_delete_update
    def delete_by_source_id(source_id: str, db: Session = None):
        result = db.execute(select(models.ADCONArea).filter_by(source_id=source_id)).one_or_none()
        if result is not None:
            db.delete(result.ADCONArea)
        else:
            return {"message": "Not Found", "errors": ["The provided area source id does not exist"]}, 404
        
    @staticmethod
    @validate_int('area_id')
    @session_handler_add_delete_update
    def delete_by_area_id(area_id: int, db: Session = None):
        result = db.execute(select(models.ADCONArea).filter_by(area_id=area_id)).one_or_none()
        if result is not None:
            db.delete(result.ADCONArea)
        else:
            return {"message": "Not Found", "errors": ["The provided area id does not exist"]}, 404
             
class ADCONRtus:

    @staticmethod
    @session_handler_add_delete_update
    def add(rtu: schemas.ADCONRtusCreate, db: Session = None):
        new_rtu = models.ADCONRtus(rtu_id=rtu.rtu_id, area_id=rtu.area_id, source_id=rtu.source_id, name=rtu.name, template=rtu.template, main_class=rtu.main_class,
                                   sub_class=rtu.sub_class, latitude=rtu.latitude, longitude=rtu.longitude, altitude=rtu.altitude, type=rtu.type, version=rtu.version,
                                   serial=rtu.serial, code=rtu.code, time_zone=rtu.time_zone, uptime=rtu.uptime, field_id=rtu.field_id, unique_attributes=rtu.unique_attributes)
        db.add(new_rtu)

    @staticmethod
    @validate_int('area_id')
    @session_handler_query
    def get_by_area_id(area_id: int, db: Session = None):
        return db.execute(select(models.ADCONRtus).filter_by(area_id=area_id)).all()

    @staticmethod
    @validate_int('rtu_id')
    @session_handler_query
    def get_by_rtu_id(rtu_id: int, db: Session = None):
        return db.execute(select(models.ADCONRtus).filter_by(rtu_id=rtu_id)).one_or_none()

    @staticmethod
    @validate_str('source_id')
    @session_handler_query
    def get_by_source_id(source_id: str, db: Session = None):
        return db.execute(select(models.ADCONRtus).filter_by(source_id=source_id)).one_or_none()
    
    @staticmethod
    @validate_str('source_id', 'new_status')
    @validate_float('last_slot')
    @session_handler_add_delete_update
    def update_comminication_status_by_source_id(source_id: str, new_status: bool, last_slot: float, db: Session = None):
        db.execute(update(models.ADCONRtus).where(models.ADCONRtus.source_id==source_id).values(active=new_status, last_slot=last_slot))

class ADCONMonitoringDevices:

    @staticmethod
    @session_handler_add_delete_update
    def add(monitoring_device: schemas.ADCONMonitoringDevicesCreate, db: Session = None):
        new_monitoring_device = models.ADCONMonitoringDevices(monitoring_device.rtu_id, monitoring_device.source_id, monitoring_device.name, monitoring_device.measurement,
                                                              monitoring_device.template, monitoring_device.main_class, monitoring_device.sub_class, monitoring_device.type,
                                                              monitoring_device.EUID, monitoring_device.sampling_method, monitoring_device.reference_offset, monitoring_device=True)
        db.add(new_monitoring_device)

    @staticmethod
    @validate_int('area_id')
    @session_handler_query
    def get_by_area_id(area_id: int, db: Session = None):
        rtu_ids_subquery = select(models.ADCONRtus.rtu_id).where(models.ADCONRtus.area_id==area_id).subquery()
        main_query = select(models.ADCONMonitoringDevices).where(models.ADCONMonitoringDevices.rtu_id.in_(rtu_ids_subquery))
        return db.execute(main_query).scalars().all()

    @staticmethod
    @validate_int('rtu_id')
    @session_handler_query
    def get_by_rtu_id(rtu_id: int, db: Session = None):
        return db.execute(select(models.ADCONMonitoringDevices).filter_by(rtu_id=rtu_id)).all()

    @staticmethod
    @validate_str('source_id')
    @session_handler_query
    def get_by_source_id(source_id: str, db: Session = None):
        return db.execute(select(models.ADCONMonitoringDevices).filter_by(source_id=source_id)).one_or_none()

    @staticmethod
    @validate_str('measurement')
    @session_handler_query
    def get_by_measurement(measurement: str, db: Session = None):
        return db.execute(select(models.ADCONMonitoringDevices).filter_by(measurement=measurement)).all()
    
    @staticmethod
    @validate_str('source_id', 'new_status')
    @session_handler_add_delete_update
    def update_comminication_status_by_source_id(source_id: str, new_status: bool, db: Session = None):
        db.execute(update(models.ADCONMonitoringDevices).where(models.ADCONMonitoringDevices.source_id==source_id).values(active=new_status))

    @staticmethod
    @validate_str('source_id')
    @session_handler_add_delete_update
    def delete_by_source_id(source_id: int, db: Session = None):
        result = db.execute(select(models.ADCONMonitoringDevices).filter_by(source_id=source_id)).one_or_none()
        if result is not None:
            db.delete(result.ADCONADCONMonitoringDevices)
        else:
            return {"message": "Not Found", "errors": ["The provided monitoring device source id does not exist"]}, 404
        
    @staticmethod
    @validate_int('monitoring_device_id')
    @session_handler_add_delete_update
    def delete_by_source_id(monitoring_device_id: int, db: Session = None):
        result = db.execute(select(models.ADCONMonitoringDevices).filter_by(monitoring_device_id=monitoring_device_id)).one_or_none()
        if result is not None:
            db.delete(result.ADCONADCONMonitoringDevices)
        else:
            return {"message": "Not Found", "errors": ["The provided monitoring device id does not exist"]}, 404
        
class DavisWeatherStations:

    @staticmethod
    @session_handler_add_delete_update
    def add(weather_station: schemas.DavisWeatherStationsCreate, db: Session = None):
        new_weather_station = models.DavisWeatherStations(weather_station.station_id, weather_station.station_id_uuid, weather_station.station_name, weather_station.gateway_id,
                                                            weather_station.gateway_id_hex, weather_station.product_number, weather_station.active, weather_station.recording_interval,
                                                            weather_station.firmware_version, weather_station.registered_date, weather_station.subscription_end_data,
                                                            weather_station.time_zone, weather_station.latitude, weather_station.longitude, weather_station.elevation, weather_station.gateway_type,
                                                            weather_station.farm_id, weather_station.field_ids, weather_station.device_id)
        db.add(new_weather_station)

    @staticmethod
    @validate_int('station_id')
    @session_handler_query
    def get_by_station_id(station_id: int, db: Session = None):
        return db.execute(select(models.DavisWeatherStations).filter_by(station_id=station_id)).one_or_none()
    
    @staticmethod
    @validate_int('station_id_uuid')
    @session_handler_query
    def get_by_station_uuid(station_id_uuid: int, db: Session = None):
        return db.execute(select(models.DavisWeatherStations).filter_by(station_id_uuid=station_id_uuid)).one_or_none()
    
    @staticmethod
    @validate_int('device_id')
    @session_handler_query
    def get_by_device_id(device_id: int, db: Session = None):
        return db.execute(select(models.DavisWeatherStations).filter_by(device_id=device_id)).one_or_none()

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_status')
    @session_handler_add_delete_update
    def update_comminication_status_by_station_id(station_id: int, new_status: bool, db: Session = None):
        db.execute(update(models.DavisWeatherStations).where(models.DavisWeatherStations.station_id==station_id).values(active=new_status))

class DavisMonitoringDevices:

    @staticmethod
    @session_handler_add_delete_update
    def add(monitoring_device: schemas.DavisMonitoringDevicesCreate, db: Session = None):
        new_monitoring_device = models.DavisMonitoringDevices(monitoring_device.monitoring_device_id, monitoring_device.station_id, monitoring_device.station_id_uuid,
                                                              monitoring_device.measurement, monitoring_device.created_date, monitoring_device.modified_date, monitoring_device.active,
                                                              monitoring_device.latitude, monitoring_device.longitude, monitoring_device.elevation, monitoring_device.reference_offset)
        db.add(new_monitoring_device)

    @staticmethod
    @session_handler_query
    @validate_int('monitoring_device_id')
    def get_by_monitoring_device_id(monitoring_device_id: int, db: Session = None):
        db.execute(select(models.DavisMonitoringDevices).filter_by(monitoring_device_id=monitoring_device_id)).one_or_none()

    @staticmethod
    @session_handler_query
    @validate_int('station_id')
    def get_by_station_id(station_id: int, db: Session = None):
        db.execute(select(models.DavisMonitoringDevices).filter_by(station_id=station_id)).all()

    @staticmethod
    @session_handler_add_delete_update
    @validate_int('monitoring_device_id')
    def update_status_by_monitoring_device_id(monitoring_device_id: int, new_status: bool, db: Session = None):
        db.execute(update(models.DavisMonitoringDevices).where(models.DavisMonitoringDevices.monitoring_device_id==monitoring_device_id).values(active=new_status))

    @staticmethod
    @session_handler_add_delete_update
    @validate_int('monitoring_device_id')
    def update_modified_date_by_monitoring_device_id(monitoring_device_id: int, new_modified_date:float, db: Session = None):
        db.execute(update(models.DavisMonitoringDevices).where(models.DavisMonitoringDevices.monitoring_device_id==monitoring_device_id).values(modified_date=new_modified_date))

class MetricaStations:

    @staticmethod
    @session_handler_add_delete_update
    def add(station: schemas.MetricaStationsCreate, db: Session = None):
        new_station = models.MetricaStations(station.station_id, station.device_id, station.station_code, station.title, station. creation_date,
                                             station.last_update, station.latitude, station.longitude, station.elevation, station.farm_id,
                                             station.field_ids)
        db.add(new_station) 

    @staticmethod
    @validate_str('station_id')
    @session_handler_query
    def get_by_station_id(station_id: str, db: Session = None):
        return db.execute(select(models.MetricaStations).filter_by(station_id=station_id)).one_or_none()
    
    @staticmethod
    @validate_str('station_code')
    @session_handler_query
    def get_by_station_code(station_code: str, db: Session = None):
        return db.execute(select(models.MetricaStations).filter_by(station_code=station_code)).one_or_none()
    
    @staticmethod
    @validate_int('device_id')
    @session_handler_query
    def get_by_device_id(device_id: int, db: Session = None):
        return db.execute(select(models.MetricaStations).filter_by(device_id=device_id)).one_or_none()

    @staticmethod
    @validate_str('station_id','new_status')
    @session_handler_add_delete_update
    def update_comminication_status_by_station_id(station_id: str, new_update: str, db: Session = None):
        db.execute(update(models.MetricaStations).where(models.MetricaStations.station_id==station_id).values(last_update=new_update))

class MetricaMonitoringDevices:

    @staticmethod
    @session_handler_add_delete_update
    def add(monitoring_device: schemas.MetricaMonitoringDevicesCreate, db: Session = None):
        new_monitoring_device = models.MetricaMonitoringDevices(monitoring_device.monitoring_device_id, monitoring_device.station_id, monitoring_device.station_code,
                                                                monitoring_device.measurement, monitoring_device.title, monitoring_device.id_sensor_of_station,
                                                                monitoring_device.sensor_type, monitoring_device.created_date, monitoring_device.longitude, monitoring_device.latitude,
                                                                monitoring_device.elevation, monitoring_device.reference_offset)
        db.add(new_monitoring_device)

    @staticmethod
    @session_handler_query
    @validate_int('monitoring_device_id')
    def get_by_monitoring_device_id(monitoring_device_id: int, db: Session = None):
        db.execute(select(models.MetricaMonitoringDevices).filter_by(monitoring_device_id=monitoring_device_id)).one_or_none()

    @staticmethod
    @session_handler_query
    @validate_str('station_id')
    def get_by_station_id(station_id: str, db: Session = None):
        db.execute(select(models.MetricaMonitoringDevices).filter_by(station_id=station_id)).all()

class DavisApiCredentials:

    @staticmethod
    @session_handler_add_delete_update
    def add(api_cred: schemas.DavisApiCredentialsCreate, db: Session = None):
        encrypt_key_id = KeyManagementService().encrypt_data(unencrypted_text=api_cred.key_id, key_id=api_cred.key_id)
        encrypt_secrete_name = KeyManagementService().encrypt_data(unencrypted_text=api_cred.secret_name, key_id=api_cred.key_id)
        new_api_cred = models.DavisApiCredentials(station_id=api_cred.station_id, key_id=encrypt_key_id, secret_name=encrypt_secrete_name)
        db.add(new_api_cred)

    @staticmethod
    @validate_int('station_id')
    @session_handler_query
    def get_by_station_id(station_id: int, db: Session = None):
        return db.execute(select(models.DavisApiCredentials).filter_by(station_id=station_id)).one_or_none()

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_key_id')
    @session_handler_add_delete_update
    def update_key_id_by_station_id(station_id: int, new_key_id: str, db: Session = None):
        db.execute(update(models.DavisApiCredentials).where(models.DavisApiCredentials.station_id==station_id).values(key_id=new_key_id))

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_secret_name')
    @session_handler_add_delete_update
    def update_secret_name_by_station_id(station_id: int, new_secret_name: str, db: Session = None):
        db.execute(update(models.DavisApiCredentials).where(models.DavisApiCredentials.station_id==station_id).values(secret_name=new_secret_name))

    @staticmethod
    @validate_int('station_id')
    @session_handler_add_delete_update
    def delete_by_station_id(station_id: int, db: Session = None):
        result = db.execute(select(models.DavisApiCredentials).filter_by(station_id=station_id)).one_or_none()
        if result is not None:
            db.delete(result.DavisApiCredentials)
        else:
            return {"message": "Not Found", "errors": ["The provided station is does not exist"]}, 404
        
class MetricaApiCredentials:

    @staticmethod
    @session_handler_add_delete_update
    def add(api_cred: schemas.MetricaApiCredentialsCreate, db: Session = None):
        encrypt_key_id = KeyManagementService().encrypt_data(unencrypted_text=api_cred.key_id, key_id=api_cred.key_id)
        encrypt_secrete_name = KeyManagementService().encrypt_data(unencrypted_text=api_cred.secret_name, key_id=api_cred.key_id)
        new_api_cred = models.MetricaApiCredentials(station_id=api_cred.station_id, key_id=encrypt_key_id, secret_name=encrypt_secrete_name)
        db.add(new_api_cred)

    @staticmethod
    @validate_int('station_id')
    @session_handler_query
    def get_by_station_id(station_id: int, db: Session = None):
        return db.execute(select(models.MetricaApiCredentials).filter_by(station_id=station_id)).one_or_none()

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_key_id')
    @session_handler_add_delete_update
    def update_key_id_by_station_id(station_id: int, new_key_id: str, db: Session = None):
        db.execute(update(models.MetricaApiCredentials).where(models.MetricaApiCredentials.station_id==station_id).values(key_id=new_key_id))

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_secret_name')
    @session_handler_add_delete_update
    def update_secret_name_by_station_id(station_id: int, new_secret_name: str, db: Session = None):
        db.execute(update(models.MetricaApiCredentials).where(models.MetricaApiCredentials.station_id==station_id).values(secret_name=new_secret_name))

    @staticmethod
    @validate_int('station_id')
    @session_handler_add_delete_update
    def delete_by_station_id(station_id: int, db: Session = None):
        result = db.execute(select(models.MetricaApiCredentials).filter_by(station_id=station_id)).one_or_none()
        if result is not None:
            db.delete(result.MetricaApiCredentials)
        else:
            return {"message": "Not Found", "errors": ["The provided station is does not exist"]}, 404
        
class ADCONApiCredentials:

    @staticmethod
    @session_handler_add_delete_update
    def add(api_cred: schemas.ADCONApiCredentialsCreate, db: Session = None):
        encrypt_key_id = KeyManagementService().encrypt_data(unencrypted_text=api_cred.key_id, key_id=api_cred.key_id)
        encrypt_secrete_name = KeyManagementService().encrypt_data(unencrypted_text=api_cred.secret_name, key_id=api_cred.key_id)
        new_api_cred = models.ADCONApiCredentials(station_id=api_cred.station_id, key_id=encrypt_key_id, secret_name=encrypt_secrete_name)
        db.add(new_api_cred)

    @staticmethod
    @validate_int('station_id')
    @session_handler_query
    def get_by_station_id(station_id: int, db: Session = None):
        return db.execute(select(models.ADCONApiCredentials).filter_by(station_id=station_id)).one_or_none()

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_key_id')
    @session_handler_add_delete_update
    def update_key_id_by_station_id(station_id: int, new_key_id: str, db: Session = None):
        db.execute(update(models.ADCONApiCredentials).where(models.ADCONApiCredentials.station_id==station_id).values(key_id=new_key_id))

    @staticmethod
    @validate_int('station_id')
    @validate_str('new_secret_name')
    @session_handler_add_delete_update
    def update_secret_name_by_station_id(station_id: int, new_secret_name: str, db: Session = None):
        db.execute(update(models.ADCONApiCredentials).where(models.ADCONApiCredentials.station_id==station_id).values(secret_name=new_secret_name))

    @staticmethod
    @validate_int('station_id')
    @session_handler_add_delete_update
    def delete_by_station_id(station_id: int, db: Session = None):
        result = db.execute(select(models.ADCONApiCredentials).filter_by(station_id=station_id)).one_or_none()
        if result is not None:
            db.delete(result.ADCONApiCredentials)
        else:
            return {"message": "Not Found", "errors": ["The provided station is does not exist"]}, 404