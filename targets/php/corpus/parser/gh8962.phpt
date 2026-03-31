<?php

namespace Foo {
    class Bar {
        public function baz() {}
        public static function qux() {}
    }

    function quux() {}

    var_dump(\Closure::fromCallable([new Bar(), 'baz']));
    var_dump(\Closure::fromCallable([Bar::class, 'qux']));
    var_dump(\Closure::fromCallable('Foo\Bar::qux'));
    var_dump(quux(...));
}

?>