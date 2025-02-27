from pydantic import BaseModel, EmailStr
from dataclasses import dataclass
import typing as tp


class LoadedXrayConfigurationOutput(BaseModel):
    SNI: str
    SID: str
    pbk: str
    port: int
    alpn: str = "h2"


class ClientModel(BaseModel):
    id: str
    email: str
    flow: str = "xtls-rprx-vision"


class XrayConfigurationClients(BaseModel):
    clients: list[ClientModel]
    decryption: str


class XrayRealitySettingsModel(BaseModel):
    dest: str
    serverNames: list[str]
    privateKey: str
    shortIds: list[str]

    class Config:
        extra = 'ignore'


class XrayConfigurationStreamSettings(BaseModel):
    network: str
    realitySettings: XrayRealitySettingsModel
    security: str = "reality"


class XrayConfigurationInbounds(BaseModel):
    port: int
    protocol: str
    tag: str
    settings: XrayConfigurationClients
    streamSettings: XrayConfigurationStreamSettings

    class Config:
        extra = 'ignore'

class XrayConfigurationModel(BaseModel):
    inbounds: list[XrayConfigurationInbounds]

    class Config:
        extra = 'ignore'


