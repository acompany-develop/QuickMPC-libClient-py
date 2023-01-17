# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common_types/common_types.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x63ommon_types/common_types.proto\x12\x0fpb_common_types\"{\n\x11ProcedureProgress\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x10\n\x08progress\x18\x03 \x01(\x02\x12\x11\n\tcompleted\x18\x04 \x01(\x08\x12\x14\n\x07\x64\x65tails\x18\x05 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_details\"\x83\x01\n\x0bJobProgress\x12\x10\n\x08job_uuid\x18\x01 \x01(\t\x12*\n\x06status\x18\x02 \x01(\x0e\x32\x1a.pb_common_types.JobStatus\x12\x36\n\nprogresses\x18\x03 \x03(\x0b\x32\".pb_common_types.ProcedureProgress\"\x8d\x01\n\nStacktrace\x12\x31\n\x06\x66rames\x18\x01 \x03(\x0b\x32!.pb_common_types.Stacktrace.Frame\x1aL\n\x05\x46rame\x12\x17\n\x0fsource_location\x18\x01 \x01(\t\x12\x13\n\x0bsource_line\x18\x02 \x01(\x04\x12\x15\n\rfunction_name\x18\x03 \x01(\t\"\x93\x01\n\x0cJobErrorInfo\x12\x0c\n\x04what\x18\x01 \x01(\t\x12\x1c\n\x0f\x61\x64\x64itional_info\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x34\n\nstacktrace\x18\x03 \x01(\x0b\x32\x1b.pb_common_types.StacktraceH\x01\x88\x01\x01\x42\x12\n\x10_additional_infoB\r\n\x0b_stacktrace*g\n\tJobStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x12\x0b\n\x07PRE_JOB\x10\x02\x12\x0b\n\x07READ_DB\x10\x03\x12\x0b\n\x07\x43OMPUTE\x10\x04\x12\x0c\n\x08WRITE_DB\x10\x05\x12\r\n\tCOMPLETED\x10\x06*\xf1\x02\n\x11\x43omputationMethod\x12\"\n\x1e\x43OMPUTATION_METHOD_UNSPECIFIED\x10\x00\x12\x1b\n\x17\x43OMPUTATION_METHOD_MEAN\x10\x01\x12\x1f\n\x1b\x43OMPUTATION_METHOD_VARIANCE\x10\x02\x12\x1a\n\x16\x43OMPUTATION_METHOD_SUM\x10\x03\x12\x1d\n\x19\x43OMPUTATION_METHOD_CORREL\x10\x04\x12(\n$COMPUTATION_METHOD_LINEAR_REGRESSION\x10\x05\x12*\n&COMPUTATION_METHOD_LOGISTIC_REGRESSION\x10\x06\x12 \n\x1c\x43OMPUTATION_METHOD_MESH_CODE\x10\x07\x12$\n COMPUTATION_METHOD_DECISION_TREE\x10\x08\x12!\n\x1d\x43OMPUTATION_METHOD_JOIN_TABLE\x10\t*\xbd\x01\n\rPredictMethod\x12\x1e\n\x1aPREDICT_METHOD_UNSPECIFIED\x10\x00\x12$\n PREDICT_METHOD_LINEAR_REGRESSION\x10\x01\x12&\n\"PREDICT_METHOD_LOGISTIC_REGRESSION\x10\x02\x12 \n\x1cPREDICT_METHOD_DECISION_TREE\x10\x03\x12\x1c\n\x18PREDICT_METHOD_SID3_TREE\x10\x04*\x8b\x01\n\x12ShareValueTypeEnum\x12 \n\x1cSHARE_VALUE_TYPE_UNSPECIFIED\x10\x00\x12 \n\x1cSHARE_VALUE_TYPE_FIXED_POINT\x10\x01\x12\x31\n-SHARE_VALUE_TYPE_UTF_8_INTEGER_REPRESENTATION\x10\x02\x42=Z;github.com/acompany-develop/QuickMPC/src/Proto/common_typesb\x06proto3')

_JOBSTATUS = DESCRIPTOR.enum_types_by_name['JobStatus']
JobStatus = enum_type_wrapper.EnumTypeWrapper(_JOBSTATUS)
_COMPUTATIONMETHOD = DESCRIPTOR.enum_types_by_name['ComputationMethod']
ComputationMethod = enum_type_wrapper.EnumTypeWrapper(_COMPUTATIONMETHOD)
_PREDICTMETHOD = DESCRIPTOR.enum_types_by_name['PredictMethod']
PredictMethod = enum_type_wrapper.EnumTypeWrapper(_PREDICTMETHOD)
_SHAREVALUETYPEENUM = DESCRIPTOR.enum_types_by_name['ShareValueTypeEnum']
ShareValueTypeEnum = enum_type_wrapper.EnumTypeWrapper(_SHAREVALUETYPEENUM)
UNKNOWN = 0
ERROR = 1
PRE_JOB = 2
READ_DB = 3
COMPUTE = 4
WRITE_DB = 5
COMPLETED = 6
COMPUTATION_METHOD_UNSPECIFIED = 0
COMPUTATION_METHOD_MEAN = 1
COMPUTATION_METHOD_VARIANCE = 2
COMPUTATION_METHOD_SUM = 3
COMPUTATION_METHOD_CORREL = 4
COMPUTATION_METHOD_LINEAR_REGRESSION = 5
COMPUTATION_METHOD_LOGISTIC_REGRESSION = 6
COMPUTATION_METHOD_MESH_CODE = 7
COMPUTATION_METHOD_DECISION_TREE = 8
COMPUTATION_METHOD_JOIN_TABLE = 9
PREDICT_METHOD_UNSPECIFIED = 0
PREDICT_METHOD_LINEAR_REGRESSION = 1
PREDICT_METHOD_LOGISTIC_REGRESSION = 2
PREDICT_METHOD_DECISION_TREE = 3
PREDICT_METHOD_SID3_TREE = 4
SHARE_VALUE_TYPE_UNSPECIFIED = 0
SHARE_VALUE_TYPE_FIXED_POINT = 1
SHARE_VALUE_TYPE_UTF_8_INTEGER_REPRESENTATION = 2


_PROCEDUREPROGRESS = DESCRIPTOR.message_types_by_name['ProcedureProgress']
_JOBPROGRESS = DESCRIPTOR.message_types_by_name['JobProgress']
_STACKTRACE = DESCRIPTOR.message_types_by_name['Stacktrace']
_STACKTRACE_FRAME = _STACKTRACE.nested_types_by_name['Frame']
_JOBERRORINFO = DESCRIPTOR.message_types_by_name['JobErrorInfo']
ProcedureProgress = _reflection.GeneratedProtocolMessageType('ProcedureProgress', (_message.Message,), {
    'DESCRIPTOR': _PROCEDUREPROGRESS,
    '__module__': 'common_types.common_types_pb2'
    # @@protoc_insertion_point(class_scope:pb_common_types.ProcedureProgress)
})
_sym_db.RegisterMessage(ProcedureProgress)

JobProgress = _reflection.GeneratedProtocolMessageType('JobProgress', (_message.Message,), {
    'DESCRIPTOR': _JOBPROGRESS,
    '__module__': 'common_types.common_types_pb2'
    # @@protoc_insertion_point(class_scope:pb_common_types.JobProgress)
})
_sym_db.RegisterMessage(JobProgress)

Stacktrace = _reflection.GeneratedProtocolMessageType('Stacktrace', (_message.Message,), {

    'Frame': _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), {
        'DESCRIPTOR': _STACKTRACE_FRAME,
        '__module__': 'common_types.common_types_pb2'
        # @@protoc_insertion_point(class_scope:pb_common_types.Stacktrace.Frame)
    }),
    'DESCRIPTOR': _STACKTRACE,
    '__module__': 'common_types.common_types_pb2'
    # @@protoc_insertion_point(class_scope:pb_common_types.Stacktrace)
})
_sym_db.RegisterMessage(Stacktrace)
_sym_db.RegisterMessage(Stacktrace.Frame)

JobErrorInfo = _reflection.GeneratedProtocolMessageType('JobErrorInfo', (_message.Message,), {
    'DESCRIPTOR': _JOBERRORINFO,
    '__module__': 'common_types.common_types_pb2'
    # @@protoc_insertion_point(class_scope:pb_common_types.JobErrorInfo)
})
_sym_db.RegisterMessage(JobErrorInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z;github.com/acompany-develop/QuickMPC/src/Proto/common_types'
    _JOBSTATUS._serialized_start = 605
    _JOBSTATUS._serialized_end = 708
    _COMPUTATIONMETHOD._serialized_start = 711
    _COMPUTATIONMETHOD._serialized_end = 1080
    _PREDICTMETHOD._serialized_start = 1083
    _PREDICTMETHOD._serialized_end = 1272
    _SHAREVALUETYPEENUM._serialized_start = 1275
    _SHAREVALUETYPEENUM._serialized_end = 1414
    _PROCEDUREPROGRESS._serialized_start = 52
    _PROCEDUREPROGRESS._serialized_end = 175
    _JOBPROGRESS._serialized_start = 178
    _JOBPROGRESS._serialized_end = 309
    _STACKTRACE._serialized_start = 312
    _STACKTRACE._serialized_end = 453
    _STACKTRACE_FRAME._serialized_start = 377
    _STACKTRACE_FRAME._serialized_end = 453
    _JOBERRORINFO._serialized_start = 456
    _JOBERRORINFO._serialized_end = 603
# @@protoc_insertion_point(module_scope)
