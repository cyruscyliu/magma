<?php

function trigger_fatal(#[\SensitiveParameter] $unused) {
    eval("class Foo {}; class Foo {}");
}

trigger_fatal("bar");
?>