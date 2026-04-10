<?php
declare(strict_types=1);

function nonReturnFunction($bar): void {}

try {
    $result = "Hello World"
        |> 'nonReturnFunction'
        |> 'strlen';
    var_dump($result);
}
catch (Throwable $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>