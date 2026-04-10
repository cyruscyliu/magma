<?php

function trigger_fatal($unused) {
    eval("class Foo {}; class Foo {}");
}

trigger_fatal("bar");
?>