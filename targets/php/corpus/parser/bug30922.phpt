<?php
interface RecursiveFooFar extends RecursiveFooFar {}
class A implements RecursiveFooFar {}

$a = new A();
var_dump($a instanceOf A);
echo "ok\n";
?>