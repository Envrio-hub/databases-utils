from __future__ import annotations

__version__='1.6.1'
__author__=['Ioannis Tsakmakis']
__date_created__='2023-10-20'
__last_updated__='2025-03-14'

from databases_companion.enum_variables import AccountType, ApplicationType, AdviceStatus, IconType
from engine import Base
from sqlalchemy import ForeignKey, Numeric, String, JSON, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import  Mapped, mapped_column

# Users
class Users(Base):
    __tablename__ = 'users_table'

    user_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    aws_user_name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(500), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLAlchemyEnum(AccountType), nullable=False)
    subscription_expires_in: Mapped[float] = mapped_column(nullable=False)

# Devices
class IoTDevices(Base):
    __tablename__ = 'IoTdevices'

    device_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.manufacturer_id', ondelete='CASCADE'), nullable=False)
    template: Mapped[str] = mapped_column(String(60), nullable=False)
    access: Mapped[dict] = mapped_column(type_=JSON, nullable=False) # {"users":[1,3,...]}
    icon_type: Mapped[IconType] = mapped_column(SQLAlchemyEnum(IconType), nullable=False)

class Manufacturers(Base):
    __tablename__ = 'manufacturers'

    manufacturer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    api_url: Mapped[str] = mapped_column(String(50), nullable=False)
    api_version: Mapped[str] = mapped_column(String(5))
    templates: Mapped[dict] = mapped_column(type_=JSON, nullable=False) # {"category1":["template_name1","template_name2"...], "category2":["template_name1",...]}

# ADCON IoT system devices
class ADCONServer(Base):
    __tablename__ = 'adcon_servers'

    server_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id', ondelete='CASCADE'), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    template: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    main_class: Mapped[str] = mapped_column(String(20), nullable=False)
    sub_class: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    serial: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    time_zone: Mapped[str] = mapped_column(String(20), nullable=False)
    last_update: Mapped[float] = mapped_column(nullable=False)
    slot_interval: Mapped[int] = mapped_column(nullable=False)
    get_data_max_slots: Mapped[int] = mapped_column(nullable=False)
    get_data_max_nodes: Mapped[int] = mapped_column(nullable=False)

class ADCONArea(Base):
    __tablename__ = 'adcon_area'

    area_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    server_id: Mapped[int] = mapped_column(ForeignKey('adcon_servers.server_id', ondelete='CASCADE'), unique=True, nullable=False)
    source_id: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    template: Mapped[str] = mapped_column(String(20), nullable=False)
    main_class : Mapped[str] = mapped_column(String(20), nullable=False)
    sub_class : Mapped[str] = mapped_column(String(20), nullable=False)

class ADCONRtus(Base):
    __tablename__ = 'adcon_rtus'

    rtu_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id', ondelete='CASCADE'), primary_key=True)
    area_id: Mapped[int] = mapped_column(ForeignKey('adcon_area.area_id', ondelete='CASCADE'), nullable=False)
    source_id: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    template: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    main_class : Mapped[str] = mapped_column(String(20), nullable=False)
    sub_class : Mapped[str] = mapped_column(String(20), nullable=False)
    type : Mapped[str] = mapped_column(String(20), nullable=False)
    version : Mapped[str] = mapped_column(String(20), nullable=False)
    serial : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    code : Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    time_zone : Mapped[str] = mapped_column(String(20), nullable=False)  
    date: Mapped[float] = mapped_column(nullable=False)
    uptime: Mapped[str] = mapped_column(String(50), nullable=False)
    first_slot: Mapped[int] = mapped_column(nullable=True, default=None)
    last_slot: Mapped[int] = mapped_column(nullable=True, default=None)  
    active: Mapped[bool] = mapped_column(nullable=True, default=True)
    latitude: Mapped[float] = mapped_column(nullable= False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    altitude: Mapped[float] = mapped_column(nullable=False)
    field_id: Mapped[int] = mapped_column(ForeignKey('fields_registry.field_id', ondelete='SET NULL'))

class ADCONMonitoringDevices(Base):
    __tablename__ = 'adcon_monitoring_control_devices'

    monitoring_device_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rtu_id: Mapped[int] = mapped_column(ForeignKey('adcon_rtus.rtu_id', ondelete='CASCADE'))
    source_id: Mapped[str] = mapped_column(String(8), unique=True, nullable=False) 
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    measurement: Mapped[str] = mapped_column(String(20), nullable=False)
    template: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    main_class : Mapped[str] = mapped_column(String(20), nullable=False)
    sub_class : Mapped[str] = mapped_column(String(20), nullable=False)
    type : Mapped[str] = mapped_column(String(20), nullable=False)
    EUID: Mapped[str] = mapped_column(String(20), nullable=False)
    sampling_method: Mapped[str] = mapped_column(String(20), nullable=False)
    reference_offset: Mapped[float] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=True, default=True)

# DAVIS IoT system devices
class DavisWeatherStations(Base):
    __tablename__ = 'davis_weather_stations'

    station_id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id', ondelete='CASCADE'), unique=True, nullable=False)
    station_id_uuid: Mapped[int] = mapped_column(unique=True, nullable=False)
    station_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    gateway_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    gateway_id_hex: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    product_number: Mapped[str] = mapped_column(String(50), nullable=False)
    active: Mapped[bool] = mapped_column(type_=Boolean, nullable=False, default=True)
    recording_interval: Mapped[int] = mapped_column(nullable=False)
    firmware_version: Mapped[str] = mapped_column(String(20))
    registered_date: Mapped[float] = mapped_column(nullable=False)
    subscription_end_data: Mapped[float] = mapped_column(nullable=False)
    time_zone: Mapped[str] = mapped_column(String(25), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    elevation: Mapped[float] = mapped_column(nullable=False)
    gateway_type: Mapped[str] = mapped_column(String(50))
    farm_id: Mapped[int] = mapped_column(ForeignKey('farms_registry.farm_id', ondelete='SET NULL'), nullable=True)
    field_ids: Mapped[dict] = mapped_column(type_=JSON, nullable=True) # {"field_ids":[1,3,4,...]}

class DavisMonitoringDevices(Base):
    __tablename__ = 'davis_monitoring_devices'

    monitoring_device_id: Mapped[int] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey('davis_weather_stations.station_id', ondelete='CASCADE'))
    station_id_uuid: Mapped[str] = mapped_column(ForeignKey('davis_weather_stations.station_id_uuid', ondelete='CASCADE'))
    measurement: Mapped[str] = mapped_column(String(20), nullable=False)
    created_date: Mapped[float] = mapped_column(nullable=False)
    modified_date: Mapped[float] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(type_=Boolean, nullable=False, default=True)    
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    elevation: Mapped[float] = mapped_column(nullable=False)
    reference_offset: Mapped[float] = mapped_column(nullable=False)

# Metrica IoT devices
class MetricaStations(Base):
    __tablename__ = 'metrica_stations'

    station_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id', ondelete='CASCADE'), unique=True, nullable=False)
    station_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    creation_date: Mapped[str] = mapped_column(String(50), nullable=True) # Date format %Y-%m-%d %H:%M:%S e.g., 2023-04-07 06:08:03
    last_update: Mapped[str] = mapped_column(String(50), nullable=True, default=True) # Date format %d/%m/%y %H:%M:%S e.g.,  22/11/24 13:00:04
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    elevation: Mapped[float] = mapped_column(nullable=False)
    farm_id: Mapped[int] = mapped_column(ForeignKey('farms_registry.farm_id', ondelete='SET NULL'), nullable=True)
    field_ids: Mapped[dict] = mapped_column(type_=JSON, nullable=True) # {"field_ids":[1,3,4,...]}

class MetricaMonitoringDevices(Base):
    __tablename__ = 'metrica_monitoring_devices'

    monitoring_device_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    station_id: Mapped[str] = mapped_column(String(60), ForeignKey('metrica_stations.station_id', ondelete='CASCADE'), nullable=False)
    station_code: Mapped[str] = mapped_column(String(50), ForeignKey('metrica_stations.station_code'), nullable=False)
    measurement: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    id_sensor_of_station: Mapped[str] = mapped_column(String(20), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_date: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    elevation: Mapped[float] = mapped_column(nullable=False)
    reference_offset: Mapped[float] = mapped_column(nullable=False)

# Davis API Credentials
class DavisApiCredentials(Base):
    __tablename__ = 'davis_api_credentials'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    station_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id',ondelete='CASCADE'), nullable=False, unique=True)
    key_id: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)
    secret_name: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)

# Metrica API Credentials
class MetricaApiCredentials(Base):
    __tablename__ = 'metrica_api_credentials'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    station_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id',ondelete='CASCADE'), nullable=False, unique=True)
    key_id: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)
    secret_name: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)

# ADCON API Credentials
class ADCONApiCredentials(Base):
    __tablename__ = 'adcon_api_credentials'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    station_id: Mapped[int] = mapped_column(ForeignKey('IoTdevices.device_id',ondelete='CASCADE'), nullable=False, unique=True)
    key_id: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)
    secret_name: Mapped[str] = mapped_column(String(767), unique=True, nullable=False)

# Farms
class FarmsRegistry(Base):
    __tablename__ = 'farms_registry'

    farm_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id: Mapped[int] =mapped_column(ForeignKey('users_table.user_id',ondelete='CASCADE'), nullable=False)
    longitude: Mapped[float] = mapped_column(type_=Numeric(10,8), nullable=False)
    latitude: Mapped[float] = mapped_column(type_=Numeric(10,8), nullable=False)

class FieldsRegistry(Base):
    __tablename__ = 'fields_registry'
    
    field_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    farm_id: Mapped[int] = mapped_column(ForeignKey('farms_registry.farm_id',ondelete='CASCADE'), nullable=False)
    boundaries: Mapped[dict] = mapped_column(type_=JSON, nullable=False)
    soil_properties: Mapped[dict] = mapped_column(type_=JSON) # {"hydraulic":[{"depth":20,"sat":45,"fc":35,"pwp":15,"ksat":40}], "physical":[{"depth":20,"sat":45,"fc":35,"pwp":15,"ksat":40}]}}

# Applications
class Applications(Base):
    __tablename__ = "applications_registry"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    field_id: Mapped[int] =  mapped_column(ForeignKey('fields_registry.field_id',ondelete='CASCADE'), nullable=False)
    type: Mapped[ApplicationType] = mapped_column(SQLAlchemyEnum(ApplicationType), nullable=False)
    suggested_amount: Mapped[float] = mapped_column(nullable=False)
    applied_amount: Mapped[float] = mapped_column(nullable=False)
    applied_in: Mapped[float] = mapped_column(nullable=False)

# Advices
class Advices(Base):
    __tablename__ = "advices_registry"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    field_id: Mapped[int] =  mapped_column(ForeignKey('fields_registry.field_id',ondelete='CASCADE'), nullable=False)
    type: Mapped[ApplicationType] = mapped_column(SQLAlchemyEnum(ApplicationType), nullable=False)
    status: Mapped[AdviceStatus] = mapped_column(SQLAlchemyEnum(AdviceStatus), nullable=False)
    date_registered: Mapped[float] = mapped_column(nullable=False)
    date_created: Mapped[float] = mapped_column(nullable=False)
