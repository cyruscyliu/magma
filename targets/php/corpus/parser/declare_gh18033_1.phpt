<?php
class Foo {
  function __destruct() {
    declare(ticks=1);
    register_tick_function(
       function() { }
    );
    echo "In destructor\n";
  }
}

$bar = new Foo;
echo "Done\n";
?>