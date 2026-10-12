<?php

function usage1($f) {
    $f(tmpMethodParamName: null);
}

usage1([new _ZendTestClass(), 'testTmpMethodWithArgInfo']);
usage1(eval('return function (string $a, string $b): string { return $a.$b; };'));

?>