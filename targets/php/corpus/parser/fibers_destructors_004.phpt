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
        throw new \Exception(sprintf("%d exception", $id));
    }
}

$f = new Fiber(function () {
    global $f2;
    new Cycle();
    new Cycle();
    new Cycle();
    try {
        gc_collect_cycles();
    } catch (\Exception $e) {
        echo $e, "\n";
    }
    $f2->resume();
});

$f->start();

?>