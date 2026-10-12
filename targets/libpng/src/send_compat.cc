#include <cstddef>
#include <cstdint>
#include <sys/syscall.h>
#include <unistd.h>

extern "C" long __send(int fd, const void *buf, unsigned long count, int flags)
{
   return syscall(SYS_sendto, fd, buf, count, flags, nullptr, 0);
}
