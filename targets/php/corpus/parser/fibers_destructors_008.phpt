<?php

register_shutdown_function(function () {
    printf("Shutdown\n");
});

class C {
    public static $instance;
    public function __destruct() {
        $f = new Fiber(function () {
            printf("Started\n");
            Fiber::suspend();
            printf("Resumed\n");
            Fiber::suspend();
        });
        $f->start();
        $f->resume();
        // Can not suspend main fiber
        Fiber::suspend();
    }
}

C::$instance = new C();

?>