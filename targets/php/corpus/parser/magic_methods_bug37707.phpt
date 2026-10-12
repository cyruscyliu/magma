<?php
class testme {
    function __clone() {
        echo "cloned\n";
    }
}
clone new testme();
echo "NO LEAK\n";
?>