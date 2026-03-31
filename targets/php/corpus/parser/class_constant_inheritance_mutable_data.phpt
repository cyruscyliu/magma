<?php

// This would previously leak under opcache.
class A {
    const X = 'X' . self::Y;
    const Y = 'Y';
}
interface I {
    const X2 = 'X2' . self::Y2;
    const Y2 = 'Y2';
}
eval('class B extends A implements I {}');
var_dump(new B);
var_dump(B::X, B::X2);

// This should only produce one warning, not two.
class X {
    const C = 1 % 1.5;
}
class Y extends X {
}
var_dump(X::C, Y::C);
?>