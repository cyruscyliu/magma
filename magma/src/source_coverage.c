#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <dlfcn.h>

static void clang_source_coverage_handler(int signum) {
    fprintf(stderr, "DEBUG: Clang source coverage signal handler invoked (sig: %d).\n", signum);
    return exit(0);
}

static void clang_source_coverage_init(void) {
    signal(SIGSEGV, clang_source_coverage_handler);
     signal(SIGILL, clang_source_coverage_handler);
    signal(SIGSTOP, clang_source_coverage_handler);
    signal(SIGABRT, clang_source_coverage_handler);
    fprintf(stderr, "DEBUG: Clang source coverage signal handler installed.\n");
}

int __libc_start_main(
    int (*main)(int, char **, char **),
    int argc,
    char **argv,
    int (*init)(int, char **, char **),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void *stack_end)
{
    typeof(&__libc_start_main) orig = dlsym(RTLD_NEXT, "__libc_start_main");

    clang_source_coverage_init();
    return orig(main, argc, argv, init, fini, rtld_fini, stack_end);
}