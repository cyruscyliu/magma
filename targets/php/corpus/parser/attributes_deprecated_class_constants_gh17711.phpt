<?php

class C {
    #[\Deprecated(self::C)]
    const C = TEST;
}

const TEST = 'Message';
var_dump(C::C);

class D {
    #[\Deprecated(Alias::C)]
    const C = 'test';
}

class_alias('D', 'Alias');
var_dump(D::C);

?>