<?php

const Closure = [strrev(...), strlen(...)];

var_dump(Closure);

foreach (Closure as $closure) {
    var_dump($closure("abc"));
}

?>