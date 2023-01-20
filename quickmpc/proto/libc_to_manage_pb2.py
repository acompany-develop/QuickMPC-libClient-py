# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: libc_to_manage.proto
"""Generated protocol buffer code."""
from common_types import common_types_pb2 as common__types_dot_common__types__pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14libc_to_manage.proto\x12\x0clibctomanage\x1a\x1f\x63ommon_types/common_types.proto\"\x8f\x01\n\x11SendSharesRequest\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x01(\t\x12\x0e\n\x06shares\x18\x02 \x01(\t\x12\x0e\n\x06schema\x18\x03 \x03(\t\x12\x10\n\x08piece_id\x18\x04 \x01(\x05\x12\x0f\n\x07sent_at\x18\x05 \x01(\t\x12\x17\n\x0fmatching_column\x18\x06 \x01(\x05\x12\r\n\x05token\x18\x07 \x01(\t\"4\n\x12SendSharesResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\"5\n\x13\x44\x65leteSharesRequest\x12\x0f\n\x07\x64\x61taIds\x18\x01 \x03(\t\x12\r\n\x05token\x18\x02 \x01(\t\"6\n\x14\x44\x65leteSharesResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\"2\n\x10GetSchemaRequest\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"C\n\x11GetSchemaResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\x12\x0e\n\x06schema\x18\x03 \x03(\t\"9\n\tJoinOrder\x12\x0f\n\x07\x64\x61taIds\x18\x01 \x03(\t\x12\x0c\n\x04join\x18\x02 \x03(\x05\x12\r\n\x05index\x18\x03 \x03(\x05\"$\n\x05Input\x12\x0b\n\x03src\x18\x01 \x03(\x05\x12\x0e\n\x06target\x18\x02 \x03(\x05\"\xab\x01\n\x19\x45xecuteComputationRequest\x12\x35\n\tmethod_id\x18\x01 \x01(\x0e\x32\".pb_common_types.ComputationMethod\x12\r\n\x05token\x18\x02 \x01(\t\x12&\n\x05table\x18\x03 \x01(\x0b\x32\x17.libctomanage.JoinOrder\x12 \n\x03\x61rg\x18\x04 \x01(\x0b\x32\x13.libctomanage.Input\"N\n\x1a\x45xecuteComputationResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\x12\x10\n\x08job_uuid\x18\x03 \x01(\t\">\n\x1bGetComputationResultRequest\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"\xaf\x02\n\x1cGetComputationResultResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\x12\x0e\n\x06result\x18\x03 \x03(\t\x12\x15\n\rcolumn_number\x18\x04 \x01(\x05\x12*\n\x06status\x18\x05 \x01(\x0e\x32\x1a.pb_common_types.JobStatus\x12\x10\n\x08piece_id\x18\x06 \x01(\x05\x12\x33\n\x08progress\x18\x07 \x01(\x0b\x32\x1c.pb_common_types.JobProgressH\x01\x88\x01\x01\x12\x11\n\x07is_dim1\x18\x08 \x01(\x08H\x00\x12\x11\n\x07is_dim2\x18\t \x01(\x08H\x00\x12\x13\n\tis_schema\x18\n \x01(\x08H\x00\x42\r\n\x0bresult_typeB\x0b\n\t_progress\"Z\n\x15SendModelParamRequest\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12\x0e\n\x06params\x18\x02 \x03(\t\x12\x10\n\x08piece_id\x18\x03 \x01(\x05\x12\r\n\x05token\x18\x04 \x01(\t\"8\n\x16SendModelParamResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\"\xb6\x01\n\x0ePredictRequest\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12\x1c\n\x14model_param_job_uuid\x18\x02 \x01(\t\x12\x30\n\x08model_id\x18\x03 \x01(\x0e\x32\x1e.pb_common_types.PredictMethod\x12&\n\x05table\x18\x04 \x01(\x0b\x32\x17.libctomanage.JoinOrder\x12\x0b\n\x03src\x18\x05 \x03(\x05\x12\r\n\x05token\x18\x06 \x01(\t\"1\n\x0fPredictResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\"#\n\x12GetDataListRequest\x12\r\n\x05token\x18\x01 \x01(\t\"4\n\x13GetDataListResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\x12\r\n\x05is_ok\x18\x02 \x01(\x08\"8\n\x15GetElapsedTimeRequest\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"=\n\x16GetElapsedTimeResponse\x12\r\n\x05is_ok\x18\x01 \x01(\x08\x12\x14\n\x0c\x65lapsed_time\x18\x02 \x01(\x01\"9\n\x16GetJobErrorInfoRequest\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"_\n\x17GetJobErrorInfoResponse\x12\x35\n\x0ejob_error_info\x18\x01 \x01(\x0b\x32\x1d.pb_common_types.JobErrorInfo\x12\r\n\x05is_ok\x18\x02 \x01(\x08\x32\xa8\x07\n\x0cLibcToManage\x12Q\n\nSendShares\x12\x1f.libctomanage.SendSharesRequest\x1a .libctomanage.SendSharesResponse\"\x00\x12W\n\x0c\x44\x65leteShares\x12!.libctomanage.DeleteSharesRequest\x1a\".libctomanage.DeleteSharesResponse\"\x00\x12N\n\tGetSchema\x12\x1e.libctomanage.GetSchemaRequest\x1a\x1f.libctomanage.GetSchemaResponse\"\x00\x12i\n\x12\x45xecuteComputation\x12\'.libctomanage.ExecuteComputationRequest\x1a(.libctomanage.ExecuteComputationResponse\"\x00\x12q\n\x14GetComputationResult\x12).libctomanage.GetComputationResultRequest\x1a*.libctomanage.GetComputationResultResponse\"\x00\x30\x01\x12]\n\x0eSendModelParam\x12#.libctomanage.SendModelParamRequest\x1a$.libctomanage.SendModelParamResponse\"\x00\x12H\n\x07Predict\x12\x1c.libctomanage.PredictRequest\x1a\x1d.libctomanage.PredictResponse\"\x00\x12T\n\x0bGetDataList\x12 .libctomanage.GetDataListRequest\x1a!.libctomanage.GetDataListResponse\"\x00\x12]\n\x0eGetElapsedTime\x12#.libctomanage.GetElapsedTimeRequest\x1a$.libctomanage.GetElapsedTimeResponse\"\x00\x12`\n\x0fGetJobErrorInfo\x12$.libctomanage.GetJobErrorInfoRequest\x1a%.libctomanage.GetJobErrorInfoResponse\"\x00\x42\x46ZDgithub.com/acompany-develop/QuickMPC/src/Proto/LibcToManageContainerb\x06proto3')


_SENDSHARESREQUEST = DESCRIPTOR.message_types_by_name['SendSharesRequest']
_SENDSHARESRESPONSE = DESCRIPTOR.message_types_by_name['SendSharesResponse']
_DELETESHARESREQUEST = DESCRIPTOR.message_types_by_name['DeleteSharesRequest']
_DELETESHARESRESPONSE = DESCRIPTOR.message_types_by_name['DeleteSharesResponse']
_GETSCHEMAREQUEST = DESCRIPTOR.message_types_by_name['GetSchemaRequest']
_GETSCHEMARESPONSE = DESCRIPTOR.message_types_by_name['GetSchemaResponse']
_JOINORDER = DESCRIPTOR.message_types_by_name['JoinOrder']
_INPUT = DESCRIPTOR.message_types_by_name['Input']
_EXECUTECOMPUTATIONREQUEST = DESCRIPTOR.message_types_by_name['ExecuteComputationRequest']
_EXECUTECOMPUTATIONRESPONSE = DESCRIPTOR.message_types_by_name['ExecuteComputationResponse']
_GETCOMPUTATIONRESULTREQUEST = DESCRIPTOR.message_types_by_name['GetComputationResultRequest']
_GETCOMPUTATIONRESULTRESPONSE = DESCRIPTOR.message_types_by_name['GetComputationResultResponse']
_SENDMODELPARAMREQUEST = DESCRIPTOR.message_types_by_name['SendModelParamRequest']
_SENDMODELPARAMRESPONSE = DESCRIPTOR.message_types_by_name['SendModelParamResponse']
_PREDICTREQUEST = DESCRIPTOR.message_types_by_name['PredictRequest']
_PREDICTRESPONSE = DESCRIPTOR.message_types_by_name['PredictResponse']
_GETDATALISTREQUEST = DESCRIPTOR.message_types_by_name['GetDataListRequest']
_GETDATALISTRESPONSE = DESCRIPTOR.message_types_by_name['GetDataListResponse']
_GETELAPSEDTIMEREQUEST = DESCRIPTOR.message_types_by_name['GetElapsedTimeRequest']
_GETELAPSEDTIMERESPONSE = DESCRIPTOR.message_types_by_name['GetElapsedTimeResponse']
_GETJOBERRORINFOREQUEST = DESCRIPTOR.message_types_by_name['GetJobErrorInfoRequest']
_GETJOBERRORINFORESPONSE = DESCRIPTOR.message_types_by_name['GetJobErrorInfoResponse']
SendSharesRequest = _reflection.GeneratedProtocolMessageType('SendSharesRequest', (_message.Message,), {
    'DESCRIPTOR': _SENDSHARESREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.SendSharesRequest)
})
_sym_db.RegisterMessage(SendSharesRequest)

SendSharesResponse = _reflection.GeneratedProtocolMessageType('SendSharesResponse', (_message.Message,), {
    'DESCRIPTOR': _SENDSHARESRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.SendSharesResponse)
})
_sym_db.RegisterMessage(SendSharesResponse)

DeleteSharesRequest = _reflection.GeneratedProtocolMessageType('DeleteSharesRequest', (_message.Message,), {
    'DESCRIPTOR': _DELETESHARESREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.DeleteSharesRequest)
})
_sym_db.RegisterMessage(DeleteSharesRequest)

DeleteSharesResponse = _reflection.GeneratedProtocolMessageType('DeleteSharesResponse', (_message.Message,), {
    'DESCRIPTOR': _DELETESHARESRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.DeleteSharesResponse)
})
_sym_db.RegisterMessage(DeleteSharesResponse)

GetSchemaRequest = _reflection.GeneratedProtocolMessageType('GetSchemaRequest', (_message.Message,), {
    'DESCRIPTOR': _GETSCHEMAREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetSchemaRequest)
})
_sym_db.RegisterMessage(GetSchemaRequest)

GetSchemaResponse = _reflection.GeneratedProtocolMessageType('GetSchemaResponse', (_message.Message,), {
    'DESCRIPTOR': _GETSCHEMARESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetSchemaResponse)
})
_sym_db.RegisterMessage(GetSchemaResponse)

JoinOrder = _reflection.GeneratedProtocolMessageType('JoinOrder', (_message.Message,), {
    'DESCRIPTOR': _JOINORDER,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.JoinOrder)
})
_sym_db.RegisterMessage(JoinOrder)

Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), {
    'DESCRIPTOR': _INPUT,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.Input)
})
_sym_db.RegisterMessage(Input)

ExecuteComputationRequest = _reflection.GeneratedProtocolMessageType('ExecuteComputationRequest', (_message.Message,), {
    'DESCRIPTOR': _EXECUTECOMPUTATIONREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.ExecuteComputationRequest)
})
_sym_db.RegisterMessage(ExecuteComputationRequest)

ExecuteComputationResponse = _reflection.GeneratedProtocolMessageType('ExecuteComputationResponse', (_message.Message,), {
    'DESCRIPTOR': _EXECUTECOMPUTATIONRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.ExecuteComputationResponse)
})
_sym_db.RegisterMessage(ExecuteComputationResponse)

GetComputationResultRequest = _reflection.GeneratedProtocolMessageType('GetComputationResultRequest', (_message.Message,), {
    'DESCRIPTOR': _GETCOMPUTATIONRESULTREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetComputationResultRequest)
})
_sym_db.RegisterMessage(GetComputationResultRequest)

GetComputationResultResponse = _reflection.GeneratedProtocolMessageType('GetComputationResultResponse', (_message.Message,), {
    'DESCRIPTOR': _GETCOMPUTATIONRESULTRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetComputationResultResponse)
})
_sym_db.RegisterMessage(GetComputationResultResponse)

SendModelParamRequest = _reflection.GeneratedProtocolMessageType('SendModelParamRequest', (_message.Message,), {
    'DESCRIPTOR': _SENDMODELPARAMREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.SendModelParamRequest)
})
_sym_db.RegisterMessage(SendModelParamRequest)

SendModelParamResponse = _reflection.GeneratedProtocolMessageType('SendModelParamResponse', (_message.Message,), {
    'DESCRIPTOR': _SENDMODELPARAMRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.SendModelParamResponse)
})
_sym_db.RegisterMessage(SendModelParamResponse)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), {
    'DESCRIPTOR': _PREDICTREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.PredictRequest)
})
_sym_db.RegisterMessage(PredictRequest)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), {
    'DESCRIPTOR': _PREDICTRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.PredictResponse)
})
_sym_db.RegisterMessage(PredictResponse)

GetDataListRequest = _reflection.GeneratedProtocolMessageType('GetDataListRequest', (_message.Message,), {
    'DESCRIPTOR': _GETDATALISTREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetDataListRequest)
})
_sym_db.RegisterMessage(GetDataListRequest)

GetDataListResponse = _reflection.GeneratedProtocolMessageType('GetDataListResponse', (_message.Message,), {
    'DESCRIPTOR': _GETDATALISTRESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetDataListResponse)
})
_sym_db.RegisterMessage(GetDataListResponse)

GetElapsedTimeRequest = _reflection.GeneratedProtocolMessageType('GetElapsedTimeRequest', (_message.Message,), {
    'DESCRIPTOR': _GETELAPSEDTIMEREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetElapsedTimeRequest)
})
_sym_db.RegisterMessage(GetElapsedTimeRequest)

GetElapsedTimeResponse = _reflection.GeneratedProtocolMessageType('GetElapsedTimeResponse', (_message.Message,), {
    'DESCRIPTOR': _GETELAPSEDTIMERESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetElapsedTimeResponse)
})
_sym_db.RegisterMessage(GetElapsedTimeResponse)

GetJobErrorInfoRequest = _reflection.GeneratedProtocolMessageType('GetJobErrorInfoRequest', (_message.Message,), {
    'DESCRIPTOR': _GETJOBERRORINFOREQUEST,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetJobErrorInfoRequest)
})
_sym_db.RegisterMessage(GetJobErrorInfoRequest)

GetJobErrorInfoResponse = _reflection.GeneratedProtocolMessageType('GetJobErrorInfoResponse', (_message.Message,), {
    'DESCRIPTOR': _GETJOBERRORINFORESPONSE,
    '__module__': 'libc_to_manage_pb2'
    # @@protoc_insertion_point(class_scope:libctomanage.GetJobErrorInfoResponse)
})
_sym_db.RegisterMessage(GetJobErrorInfoResponse)

_LIBCTOMANAGE = DESCRIPTOR.services_by_name['LibcToManage']
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZDgithub.com/acompany-develop/QuickMPC/src/Proto/LibcToManageContainer'
    _SENDSHARESREQUEST._serialized_start = 72
    _SENDSHARESREQUEST._serialized_end = 215
    _SENDSHARESRESPONSE._serialized_start = 217
    _SENDSHARESRESPONSE._serialized_end = 269
    _DELETESHARESREQUEST._serialized_start = 271
    _DELETESHARESREQUEST._serialized_end = 324
    _DELETESHARESRESPONSE._serialized_start = 326
    _DELETESHARESRESPONSE._serialized_end = 380
    _GETSCHEMAREQUEST._serialized_start = 382
    _GETSCHEMAREQUEST._serialized_end = 432
    _GETSCHEMARESPONSE._serialized_start = 434
    _GETSCHEMARESPONSE._serialized_end = 501
    _JOINORDER._serialized_start = 503
    _JOINORDER._serialized_end = 560
    _INPUT._serialized_start = 562
    _INPUT._serialized_end = 598
    _EXECUTECOMPUTATIONREQUEST._serialized_start = 601
    _EXECUTECOMPUTATIONREQUEST._serialized_end = 772
    _EXECUTECOMPUTATIONRESPONSE._serialized_start = 774
    _EXECUTECOMPUTATIONRESPONSE._serialized_end = 852
    _GETCOMPUTATIONRESULTREQUEST._serialized_start = 854
    _GETCOMPUTATIONRESULTREQUEST._serialized_end = 916
    _GETCOMPUTATIONRESULTRESPONSE._serialized_start = 919
    _GETCOMPUTATIONRESULTRESPONSE._serialized_end = 1222
    _SENDMODELPARAMREQUEST._serialized_start = 1224
    _SENDMODELPARAMREQUEST._serialized_end = 1314
    _SENDMODELPARAMRESPONSE._serialized_start = 1316
    _SENDMODELPARAMRESPONSE._serialized_end = 1372
    _PREDICTREQUEST._serialized_start = 1375
    _PREDICTREQUEST._serialized_end = 1557
    _PREDICTRESPONSE._serialized_start = 1559
    _PREDICTRESPONSE._serialized_end = 1608
    _GETDATALISTREQUEST._serialized_start = 1610
    _GETDATALISTREQUEST._serialized_end = 1645
    _GETDATALISTRESPONSE._serialized_start = 1647
    _GETDATALISTRESPONSE._serialized_end = 1699
    _GETELAPSEDTIMEREQUEST._serialized_start = 1701
    _GETELAPSEDTIMEREQUEST._serialized_end = 1757
    _GETELAPSEDTIMERESPONSE._serialized_start = 1759
    _GETELAPSEDTIMERESPONSE._serialized_end = 1820
    _GETJOBERRORINFOREQUEST._serialized_start = 1822
    _GETJOBERRORINFOREQUEST._serialized_end = 1879
    _GETJOBERRORINFORESPONSE._serialized_start = 1881
    _GETJOBERRORINFORESPONSE._serialized_end = 1976
    _LIBCTOMANAGE._serialized_start = 1979
    _LIBCTOMANAGE._serialized_end = 2915
# @@protoc_insertion_point(module_scope)
