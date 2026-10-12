<?php
class Foo {
    public function __destruct() {
        throw new \Exception(__METHOD__);
    }
}

set_exception_handler(function (\Throwable $exception) {
    echo 'Caught: ' . $exception->getMessage() . "\n";
});

const FOO = new Foo;
?>