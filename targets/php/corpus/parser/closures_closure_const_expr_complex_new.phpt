<?php

class Dummy {
  public function __construct(
      public Closure $c,
  ) {}
}

const Closure = new Dummy(static function () {
  echo "called", PHP_EOL;
});

var_dump(Closure);

(Closure->c)();

?>