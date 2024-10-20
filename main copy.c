#include "work.h"

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: main <last 5 digits of your reg. no>\n");
    return EXIT_FAILURE;
  }
  work_init(atoi(argv[1]));

  // Put your changes here

  if (work_run() == 0) {
    printf("Work completed successfully\n");
  }

  return 0;
}
