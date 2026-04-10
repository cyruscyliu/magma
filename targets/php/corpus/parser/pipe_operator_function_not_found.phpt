<?php

try {
    $res1 = 5 |> '_test';
}
catch (Throwable $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>