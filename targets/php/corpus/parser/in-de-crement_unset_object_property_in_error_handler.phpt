<?php
class C {
    public $a;

    public function errorHandler($errno, $errstr) {
        var_dump($errstr);
        unset($this->a);
    }
}

$c = new C;
set_error_handler([$c, 'errorHandler']);

/* default property value */
var_dump(--$c->a);

echo "NULL (only --)\n";
echo "POST DEC\n";
$c->a = null;
var_dump($c->a--);
unset($c->a);
echo "PRE DEC\n";
$c->a = null;
var_dump(--$c->a);
unset($c->a);
echo "Empty string\n";
echo "POST INC\n";
$c->a = "";
var_dump($c->a++);
unset($c->a);
echo "POST DEC\n";
$c->a = "";
var_dump($c->a--);
unset($c->a);
echo "PRE INC\n";
$c->a = "";
var_dump(++$c->a);
unset($c->a);
echo "PRE DEC\n";
$c->a = "";
var_dump(--$c->a);
unset($c->a);
echo "Non fill ASCII (only ++)\n";
echo "POST INC\n";
$c->a = " ad ";
var_dump($c->a++);
unset($c->a);
echo "PRE INC\n";
$c->a = " ad ";
var_dump(++$c->a);
unset($c->a);
echo "Bool\n";
echo "POST INC\n";
$c->a = false;
var_dump($c->a++);
unset($c->a);
echo "POST DEC\n";
$c->a = false;
var_dump($c->a--);
unset($c->a);
echo "PRE INC\n";
$c->a = false;
var_dump(++$c->a);
unset($c->a);
echo "PRE DEC\n";
$c->a = false;
var_dump(--$c->a);
unset($c->a);
echo "POST INC\n";
$c->a = true;
var_dump($c->a++);
unset($c->a);
echo "POST DEC\n";
$c->a = true;
var_dump($c->a--);
unset($c->a);
echo "PRE INC\n";
$c->a = true;
var_dump(++$c->a);
unset($c->a);
echo "PRE DEC\n";
$c->a = true;
var_dump(--$c->a);
unset($c->a);
?>