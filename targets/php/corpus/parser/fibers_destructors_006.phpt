<?php

register_shutdown_function(function () {
    printf("Shutdown\n");
});

class Cycle {
    public static $counter = 0;
    public $self;
    public function __construct() {
        $this->self = $this;
    }
    public function __destruct() {
        $id = self::$counter++;
        printf("%d: Start destruct\n", $id);
        if ($id === 0) {
            global $f2;
            $f2 = Fiber::getCurrent();
            Fiber::suspend(new stdClass);
        }
        printf("%d: End destruct\n", $id);
    }
}

$f = new Fiber(function () {
    new Cycle();
    new Cycle();
    gc_collect_cycles();
});

$f->start();

new Cycle();
new Cycle();
gc_collect_cycles();

$f2->resume();

?>