import ctypes

class MemoryStatus(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),('total',ctypes.c_ulonglong),('available',ctypes.c_ulonglong),('total_page',ctypes.c_ulonglong),('available_page',ctypes.c_ulonglong),('total_virtual',ctypes.c_ulonglong),('available_virtual',ctypes.c_ulonglong),('extended',ctypes.c_ulonglong)]
m=MemoryStatus()
m.length=ctypes.sizeof(m)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
print('memory_load_percent',m.load,'total_gb',round(m.total/2**30,2),'available_gb',round(m.available/2**30,2))
