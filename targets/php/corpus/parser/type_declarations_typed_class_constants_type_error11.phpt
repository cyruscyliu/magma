<?php
enum E1 {
    const static C = E2::Foo;
}

enum E2 {
   case Foo;
}

try {
    var_dump(E1::C);
} catch (TypeError $e) {
    echo $e->getMessage() . "\n";
}

?>