<?php

register_shutdown_function(function () {
    printf("Shutdown\n");
});

class Cycle {
    public static $counter = 0;
    public function __destruct() {
        $id = self::$counter++;
        printf("%d: Start destruct\n", $id);
        switch ($id) {
            case 0:
                global $f2;
                $f2 = Fiber::getCurrent();
                Fiber::suspend(new stdClass);
                break;
            case 1:
                $f3 = new Fiber(function () use ($id) {
                    printf("%d: Fiber\n", $id);
                });
                $f3->start();
                break;
            case 2:
                global $f2;
                $f2->resume();
                break;
        }
        printf("%d: End destruct\n", $id);
    }
}

$f = new Fiber(function () {
    new Cycle();
});

$f->start();

new Cycle();
new Cycle();

?>