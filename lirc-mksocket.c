#include <sys/socket.h>
#include <sys/un.h>

struct sockaddr_un sun;
int sock;

int
main(int ac, char **av)
{
  sun.sun_family=AF_UNIX;
  strcpy(sun.sun_path,av[1]);
  sock=socket(PF_LOCAL, SOCK_STREAM, 0);
  bind(sock,(struct sockaddr*)&sun,SUN_LEN(&sun));
  return 0;
}
