<?php

interface A {}
interface B {}

function test(): object|(A&B) {}

?>
===DONE===