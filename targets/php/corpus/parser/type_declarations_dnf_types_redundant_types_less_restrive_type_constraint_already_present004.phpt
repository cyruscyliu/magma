<?php

interface A {}
interface B {}
interface C {}

function test(): (A&B&C)|(A&B) {}

?>
===DONE===