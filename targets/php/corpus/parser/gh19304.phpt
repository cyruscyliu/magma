<?php

$foo = new class {
    public self $v;
};

try {
    $foo->v = 0;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>