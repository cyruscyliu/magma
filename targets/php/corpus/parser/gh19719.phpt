<?php
// e.g some comments
?>
<?php

declare(strict_types=1);

function takesInt(int $x) {}

try {
    takesInt('42');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>