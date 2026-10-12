<?php

function foo()     { echo __FUNCTION__, PHP_EOL; return 1; }
function bar()     { echo __FUNCTION__, PHP_EOL; return false; }
function baz($in)  { echo __FUNCTION__, PHP_EOL; return $in; }
function quux($in) { echo __FUNCTION__, PHP_EOL; throw new \Exception('Oops'); }

try {
    $result = foo()
        |> (bar() ? baz(...) : quux(...))
        |> var_dump(...);
}
catch (Throwable $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

try {
    $result = foo()
      |> (throw new Exception('Break'))
      |> (bar() ? baz(...) : quux(...))
      |> var_dump(...);
}
catch (Throwable $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>