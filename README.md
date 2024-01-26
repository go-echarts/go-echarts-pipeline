<p align="center">
	<img src="https://user-images.githubusercontent.com/19553554/52535979-c0d0e680-2d8f-11e9-85c8-2e9f659e7c6f.png" width=300 height=300 />
</p>

<h1 align="center">go-echarts-pipeline</h1>
<p align="center">
    <em> 🍄️ The integration pipeline for go-echarts.</em>
</p>


> The `go-echarts-pipeline` is made for the integration test.

# How to

In this integration test, it will `clone` both `go-echarts/go-echarts`
and `go-echarts/examples` repo.
The `go-echarts/examples` contains lots of showcases, it can be the test cases also.

Idea of this pipeline is that we can compare the generated content (with latest `go-echarts` codebase)
with the snapshot content (with latest `go-echarts` release) to distinguish any changes.

Technically, it will mask all the `Rand` mock things such as `numbers`, `chartID`...etc, then
checking the generated options must be same (same keys, same structure).

If something's wrong, it will output the `diff` details. i.e.

```shell
------------------------------
Compare files failed with bar.html
Find different options from generated_content to snapshot_content : 
 
- <script type="text/javascript">
+ <script2333 type="text/javascript">
- </script>
+ </scri123pt>

-------------------------------

```

# License

MIT [@Koooooo-7](https://github.com/Koooooo-7)