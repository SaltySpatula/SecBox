# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: syscall.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import protos.common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rsyscall.proto\x12\x0egvisor.syscall\x1a\x0c\x63ommon.proto\"\'\n\x04\x45xit\x12\x0e\n\x06result\x18\x01 \x01(\x03\x12\x0f\n\x07\x65rrorno\x18\x02 \x01(\x03\"\xc2\x01\n\x07Syscall\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x04 \x01(\x04\x12\x0c\n\x04\x61rg1\x18\x05 \x01(\x04\x12\x0c\n\x04\x61rg2\x18\x06 \x01(\x04\x12\x0c\n\x04\x61rg3\x18\x07 \x01(\x04\x12\x0c\n\x04\x61rg4\x18\x08 \x01(\x04\x12\x0c\n\x04\x61rg5\x18\t \x01(\x04\x12\x0c\n\x04\x61rg6\x18\n \x01(\x04\"\xb7\x01\n\x04Open\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x10\n\x08pathname\x18\x06 \x01(\t\x12\r\n\x05\x66lags\x18\x07 \x01(\r\x12\x0c\n\x04mode\x18\x08 \x01(\r\"\x89\x01\n\x05\x43lose\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\"\x97\x01\n\x04Read\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\r\n\x05\x63ount\x18\x06 \x01(\x04\"\x9c\x01\n\x07\x43onnect\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\x0c\"\xc7\x01\n\x06\x45xecve\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x10\n\x08pathname\x18\x06 \x01(\t\x12\x0c\n\x04\x61rgv\x18\x07 \x03(\t\x12\x0c\n\x04\x65nvv\x18\x08 \x03(\t\x12\r\n\x05\x66lags\x18\t \x01(\r\"\x9d\x01\n\x06Socket\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0e\n\x06\x64omain\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\x05\x12\x10\n\x08protocol\x18\x06 \x01(\x05\"\x9b\x01\n\x05\x43hdir\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x03\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x10\n\x08pathname\x18\x06 \x01(\t\"\x99\x01\n\x08Setresid\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0c\n\x04rgid\x18\x04 \x01(\r\x12\x0c\n\x04\x65gid\x18\x05 \x01(\r\x12\x0c\n\x04sgid\x18\x06 \x01(\r\"x\n\x05Setid\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02id\x18\x04 \x01(\r\"(\n\x0cStructRlimit\x12\x0b\n\x03\x63ur\x18\x01 \x01(\x04\x12\x0b\n\x03max\x18\x02 \x01(\x04\"\xef\x01\n\x07Prlimit\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0b\n\x03pid\x18\x04 \x01(\x05\x12\x10\n\x08resource\x18\x05 \x01(\x03\x12/\n\tnew_limit\x18\x06 \x01(\x0b\x32\x1c.gvisor.syscall.StructRlimit\x12/\n\told_limit\x18\x07 \x01(\x0b\x32\x1c.gvisor.syscall.StructRlimit\"\x9a\x01\n\x04Pipe\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\r\n\x05\x66lags\x18\x04 \x01(\r\x12\x0e\n\x06reader\x18\x05 \x01(\x05\x12\x0e\n\x06writer\x18\x06 \x01(\x05\"\xa4\x01\n\x05\x46\x63ntl\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x0b\n\x03\x63md\x18\x06 \x01(\x05\x12\x0c\n\x04\x61rgs\x18\x07 \x01(\x03\"\xaa\x01\n\x03\x44up\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0e\n\x06old_fd\x18\x04 \x01(\x05\x12\x0e\n\x06new_fd\x18\x05 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x06 \x01(\t\x12\r\n\x05\x66lags\x18\x07 \x01(\r\"\xab\x01\n\x08Signalfd\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x0e\n\x06sigset\x18\x06 \x01(\x04\x12\r\n\x05\x66lags\x18\x07 \x01(\x05\"\x7f\n\x06\x43hroot\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x10\n\x08pathname\x18\x04 \x01(\t\"\x8a\x01\n\x07\x45ventfd\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0b\n\x03val\x18\x04 \x01(\x05\x12\r\n\x05\x66lags\x18\x05 \x01(\r\"\xa8\x01\n\x05\x43lone\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\r\n\x05\x66lags\x18\x04 \x01(\x04\x12\r\n\x05stack\x18\x05 \x01(\x04\x12\x0f\n\x07new_tid\x18\x06 \x01(\x04\x12\x0b\n\x03tls\x18\x07 \x01(\x04\"\x99\x01\n\x04\x42ind\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\x0c\"\xaa\x01\n\x06\x41\x63\x63\x65pt\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\x0c\x12\r\n\x05\x66lags\x18\x07 \x01(\x05\"\x95\x01\n\rTimerfdCreate\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x10\n\x08\x63lock_id\x18\x04 \x01(\x05\x12\r\n\x05\x66lags\x18\x05 \x01(\x05\"%\n\x08Timespec\x12\x0b\n\x03sec\x18\x01 \x01(\x03\x12\x0c\n\x04nsec\x18\x02 \x01(\x03\"a\n\nItimerSpec\x12*\n\x08interval\x18\x01 \x01(\x0b\x32\x18.gvisor.syscall.Timespec\x12\'\n\x05value\x18\x02 \x01(\x0b\x32\x18.gvisor.syscall.Timespec\"\xff\x01\n\x0eTimerfdSetTime\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\r\n\x05\x66lags\x18\x06 \x01(\x05\x12-\n\tnew_value\x18\x07 \x01(\x0b\x32\x1a.gvisor.syscall.ItimerSpec\x12-\n\told_value\x18\x08 \x01(\x0b\x32\x1a.gvisor.syscall.ItimerSpec\"\xc1\x01\n\x0eTimerfdGetTime\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12-\n\tcur_value\x18\x06 \x01(\x0b\x32\x1a.gvisor.syscall.ItimerSpec\"k\n\x04\x46ork\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\"\x81\x01\n\x0bInotifyInit\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\r\n\x05\x66lags\x18\x04 \x01(\x05\"\xb3\x01\n\x0fInotifyAddWatch\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\x10\n\x08pathname\x18\x06 \x01(\t\x12\x0c\n\x04mask\x18\x07 \x01(\r\"\x9e\x01\n\x0eInotifyRmWatch\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\n\n\x02\x66\x64\x18\x04 \x01(\x05\x12\x0f\n\x07\x66\x64_path\x18\x05 \x01(\t\x12\n\n\x02wd\x18\x06 \x01(\x05\"\xc3\x01\n\nSocketPair\x12\x30\n\x0c\x63ontext_data\x18\x01 \x01(\x0b\x32\x1a.gvisor.common.ContextData\x12\"\n\x04\x65xit\x18\x02 \x01(\x0b\x32\x14.gvisor.syscall.Exit\x12\r\n\x05sysno\x18\x03 \x01(\x04\x12\x0e\n\x06\x64omain\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\x05\x12\x10\n\x08protocol\x18\x06 \x01(\x05\x12\x0f\n\x07socket1\x18\x07 \x01(\x05\x12\x0f\n\x07socket2\x18\x08 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'syscall_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EXIT._serialized_start=47
  _EXIT._serialized_end=86
  _SYSCALL._serialized_start=89
  _SYSCALL._serialized_end=283
  _OPEN._serialized_start=286
  _OPEN._serialized_end=469
  _CLOSE._serialized_start=472
  _CLOSE._serialized_end=609
  _READ._serialized_start=612
  _READ._serialized_end=763
  _CONNECT._serialized_start=766
  _CONNECT._serialized_end=922
  _EXECVE._serialized_start=925
  _EXECVE._serialized_end=1124
  _SOCKET._serialized_start=1127
  _SOCKET._serialized_end=1284
  _CHDIR._serialized_start=1287
  _CHDIR._serialized_end=1442
  _SETRESID._serialized_start=1445
  _SETRESID._serialized_end=1598
  _SETID._serialized_start=1600
  _SETID._serialized_end=1720
  _STRUCTRLIMIT._serialized_start=1722
  _STRUCTRLIMIT._serialized_end=1762
  _PRLIMIT._serialized_start=1765
  _PRLIMIT._serialized_end=2004
  _PIPE._serialized_start=2007
  _PIPE._serialized_end=2161
  _FCNTL._serialized_start=2164
  _FCNTL._serialized_end=2328
  _DUP._serialized_start=2331
  _DUP._serialized_end=2501
  _SIGNALFD._serialized_start=2504
  _SIGNALFD._serialized_end=2675
  _CHROOT._serialized_start=2677
  _CHROOT._serialized_end=2804
  _EVENTFD._serialized_start=2807
  _EVENTFD._serialized_end=2945
  _CLONE._serialized_start=2948
  _CLONE._serialized_end=3116
  _BIND._serialized_start=3119
  _BIND._serialized_end=3272
  _ACCEPT._serialized_start=3275
  _ACCEPT._serialized_end=3445
  _TIMERFDCREATE._serialized_start=3448
  _TIMERFDCREATE._serialized_end=3597
  _TIMESPEC._serialized_start=3599
  _TIMESPEC._serialized_end=3636
  _ITIMERSPEC._serialized_start=3638
  _ITIMERSPEC._serialized_end=3735
  _TIMERFDSETTIME._serialized_start=3738
  _TIMERFDSETTIME._serialized_end=3993
  _TIMERFDGETTIME._serialized_start=3996
  _TIMERFDGETTIME._serialized_end=4189
  _FORK._serialized_start=4191
  _FORK._serialized_end=4298
  _INOTIFYINIT._serialized_start=4301
  _INOTIFYINIT._serialized_end=4430
  _INOTIFYADDWATCH._serialized_start=4433
  _INOTIFYADDWATCH._serialized_end=4612
  _INOTIFYRMWATCH._serialized_start=4615
  _INOTIFYRMWATCH._serialized_end=4773
  _SOCKETPAIR._serialized_start=4776
  _SOCKETPAIR._serialized_end=4971
# @@protoc_insertion_point(module_scope)
