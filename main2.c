#include "work.h"
#include <sys/mman.h>  // For mmap and related constants
#include <unistd.h>    // For system constants like PAGE_SIZE
#include <errno.h>     // For errno
#include <stdio.h>
#include <stdlib.h>

#define PAGE_SIZE (2 * 1024 * 1024) // 2MB page size

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: main <last 5 digits of your reg. no>\n");
    return EXIT_FAILURE;
  }
  work_init(atoi(argv[1]));

  // Put your changes here

  // Open the file containing the base addresses for large pages (produced by analyze.py)
  FILE *fp = fopen("largepages.txt", "r");
  if (fp == NULL) {
    fprintf(stderr, "Error: Could not open largepages.txt\n");
    return EXIT_FAILURE;
  }

  // Allocate memory for up to 8 large pages (as instructed)
  int num_pages = 0;
  unsigned long base_address;

  // Read each base address from the file
  while (fscanf(fp, "%lu", &base_address) == 1 && num_pages < 8) {
    // Attempt to map a 2MB large page at the base address
    void *mapped_address = mmap((void *)base_address, PAGE_SIZE, PROT_READ | PROT_WRITE,
                                MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED | MAP_HUGETLB, -1, 0);
    
    if (mapped_address == MAP_FAILED) {
      fprintf(stderr, "Error: mmap failed at address %lu, errno = %d\n", base_address, errno);
      fclose(fp);
      return EXIT_FAILURE;
    }

    num_pages++; // Increment the page count
  }

  fclose(fp);

  // End of your changes

  if (work_run() == 0) {
    printf("Work completed successfully\n");
  }

  return 0;
}
