<?php

class T {
    public function __construct(
        private(set) string $prop,
    ) {}
}
var_dump(new T('Test'));

?>