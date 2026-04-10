<?php

readonly class C {
    public function __construct(
        public int $prop { set => $value; },
    ) {}
}

?>