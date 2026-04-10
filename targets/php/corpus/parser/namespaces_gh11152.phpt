<?php

namespace string;

use string as StringAlias;

class C {}

function test(StringAlias\C $o) {
    var_dump($o::class);
}

test(new C());

?>