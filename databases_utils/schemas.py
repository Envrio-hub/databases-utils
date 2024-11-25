__version__='1.4.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2023-10-20'
__last_updated__='2024-11-22'

from pydantic import BaseModel
from .enum_variables import AccountType, IconType

# Base Models
class UsersTableBase(BaseModel):
    aws_user_name: str
    email: str
    account_type: AccountType
    subscription_expires_in: float

class IoTDevicesBase(BaseModel):
    manufacturer_id: int
    access: dict
    icon_type: IconType

class ManufacturersBase(BaseModel):
    name: str
    api_url: str
    api_version: str
    templates: dict

class ADCONServerBase(BaseModel):
    server_id: int
    source_id: str
    template: str
    name: str
    main_class: str
    sub_class: str
    type: str
    version: str
    serial: str
    code: str
    time_zone: str
    last_update: float
    slot_interval: int
    get_data_max_slots: int
    get_data_max_nodes: int

class ADCONAreaBase(BaseModel):
    server_id: int
    source_id: str
    name: str
    template: str
    main_class : str
    sub_class : str

class ADCONRtusBase(BaseModel):
    rtu_id: int
    area_id: int
    source_id: str
    name: str
    template: str
    main_class : str
    sub_class : str
    latitude: float
    longitude: float
    altitude: float
    type : str
    version : str
    serial : str
    code : str
    time_zone : str
    uptime: str
    field_id: int
    unique_attributes: dict

class ADCONMonitoringDevicesBase(BaseModel):
    rtu_id: int
    source_id: str
    name: str
    measurement: str
    template: str
    main_class : str
    sub_class : str
    type : str
    EUID: str
    sampling_method: str
    reference_offset: float
    active: bool

class DavisWeatherStationsBase(BaseModel):
    station_id: int
    device_id: int
    station_id_uuid: int
    station_name: str
    gateway_id: int
    gateway_id_hex: str
    product_number: str
    active: bool
    recording_interval: int
    firmware_version: str
    registered_date: float
    subscription_end_data: float
    time_zone: str
    latitude: float
    longitude: float
    elevation: float
    gateway_type: str
    farm_id: int
    field_ids: dict

class DavisMonitoringDevicesBase(BaseModel):
    monitoring_device_id: int
    station_id: int
    station_id_uuid: str
    measurement: str
    created_date: float
    modified_date: float
    active: bool
    latitude: float
    longitude: float
    elevation: float
    reference_offset: float

class MetricaStationsBase(BaseModel):
    station_id: str
    device_id: int
    station_code: str
    title: str
    creation_date: str
    last_update: str
    latitude: float
    longitude: float
    elevation: float
    farm_id: int
    field_ids: dict

class MetricaMonitoringDevicesBase(BaseModel):
    monitoring_device_id: str
    station_id: str
    station_code: str
    measurement: str
    title: str
    id_sensor_of_station: str
    sensor_type: str
    created_date: float
    latitude: float
    longitude: float
    elevation: float
    reference_offset: float

class DavisApiCredentialsBase(BaseModel):
    station_id: int
    key_id: str
    secret_name: str

class MetricaApiCredentialsBase(BaseModel):
    station_id: int
    key_id: str
    secret_name: str

class ADCONApiCredentialsBase(BaseModel):
    station_id: int
    key_id: str
    secret_name: str

class FarmsRegistryBase(BaseModel):
    user_id: int
    longitude: float
    latitude: float

class FieldsRegistyBase(BaseModel):
    farm_id: int
    boundaries: dict
    soil_properties: dict

class ApplicationsBase(BaseModel):
    field_id: int
    type: str
    suggested_amount: dict
    applied_amount: dict
    applied_in: float

class AdvicesBase(BaseModel):
    field_id: int
    type: str
    status: str
    date_registered: float
    date_created: float

# Create Models

class UsersTableCreate(UsersTableBase):
    pass

class IoTDevicesCreate(IoTDevicesBase):
    pass

class ManufacturersCreate(ManufacturersBase):
    pass

class ADCONServerCreate(ADCONServerBase):
    pass

class ADCONAreaCreate(ADCONAreaBase):
    pass

class ADCONRtusCreate(ADCONRtusBase):
    pass

class ADCONMonitoringDevicesCreate(ADCONMonitoringDevicesBase):
    pass

class DavisWeatherStationsCreate(DavisWeatherStationsBase):
    pass

class DavisMonitoringDevicesCreate(DavisMonitoringDevicesBase):
    pass

class MetricaStationsCreate(MetricaStationsBase):
    pass

class MetricaMonitoringDevicesCreate(MetricaMonitoringDevicesBase):
    pass

class DavisApiCredentialsCreate(DavisApiCredentialsBase):
    pass

class MetricaApiCredentialsCreate(MetricaApiCredentialsBase):
    pass

class ADCONApiCredentialsCreate(ADCONApiCredentialsBase):
    pass

class FarmsRegistryCreate(FarmsRegistryBase):
    pass

class FieldsRegistyCreate(FieldsRegistyBase):
    pass

class ApplicationsCreate(ApplicationsBase):
    pass

class AdvicesCreate(AdvicesBase):
    pass

