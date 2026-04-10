<?php

$readonly_anon = new #[AllowDynamicProperties] readonly class {
    public int $field;
    function __construct() {
        $this->field = 2;
    }
};

?>