<?php

ob_start(function() {
    global $a;
    for ($i = count($a); $i > 0; --$i) {
        $a[] = 2;
    }
    fwrite(STDOUT, "Success");
});

$a = [];
// trigger OOM in a resize operation
while (1) {
    $a[] = 1;
}

?>