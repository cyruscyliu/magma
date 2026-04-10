<?php
function error_handler($num, $msg, $file, $line) {
    echo $line,"\n";
}
set_error_handler('error_handler');
trigger_error("line", E_USER_WARNING);
$x = <<<EOF
EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
$x = <<<'EOF'
EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
$x = <<<EOF
test
EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
$x = <<<'EOF'
test
EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
$x = <<<EOF
test1
test2

test3


EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
$x = <<<'EOF'
test1
test2

test3


EOF;
var_dump($x);
trigger_error("line", E_USER_WARNING);
echo "ok\n";
?>