<?php

function a() {
    yield from a();
}

foreach(a() as $v);
?>