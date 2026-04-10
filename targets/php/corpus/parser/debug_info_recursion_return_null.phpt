<?php

set_error_handler(
    static function () {
        echo "in handler\n";
        $f = new Foo();
        var_dump($f);
    }
);

class Foo {
  public function __debugInfo() {
    return null;
  }
}

$f = new Foo;
var_dump($f);

?>