<?php

namespace NameSpaceName {
    class ClassName {
        public function methodName() {
            $c = function () {};
            $r = new \ReflectionFunction($c);
            var_dump($r->name);
        }

        public function nestedClosure() {
            $c = function () {
                $c = function () {
                    $c = function () {};
                    $r = new \ReflectionFunction($c);
                    var_dump($r->name);
                };

                $c();
            };

            $c();
        }
    }

    function function_name() {
        $c = function () { };
        $r = new \ReflectionFunction($c);
        var_dump($r->name);
    }
}

namespace {
    class ClassName {
        public function methodName() {
            $c = function () {};
            $r = new \ReflectionFunction($c);
            var_dump($r->name);
        }

        public function nestedClosure() {
            $c = function () {
                $c = function () {
                    $c = function () {};
                    $r = new \ReflectionFunction($c);
                    var_dump($r->name);
                };

                $c();
            };

            $c();
        }
    }

    function function_name() {
        $c = function () { };
        $r = new \ReflectionFunction($c);
        var_dump($r->name);
    }

    $class = new \NameSpaceName\ClassName();
    $class->methodName();
    $class->nestedClosure();
    \NameSpaceName\function_name();

    $class = new \ClassName();
    $class->methodName();
    $class->nestedClosure();
    \function_name();

    $c = function () { };
    $r = new \ReflectionFunction($c);
    var_dump($r->name);
}

?>