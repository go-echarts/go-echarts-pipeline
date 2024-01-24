<p align="center">
	<img src="https://user-images.githubusercontent.com/19553554/52535979-c0d0e680-2d8f-11e9-85c8-2e9f659e7c6f.png" width=300 height=300 />
</p>

<h1 align="center">go-echarts-pipeline</h1>
<p align="center">
    <em> 🍄️ The integration pipeline for go-echarts.</em>
</p>


> The `go-echarts-pipeline` is made for the integration test.

# How to

In this integration test, it will `close` both `go-echarts/go-echarts`
and `go-echarts/examples` repo.
The `go-echarts/examples` contains lots of showcases, it can be the test cases also.
Assumptions of this pipeline is we could compare the generated content (with latest `go-echarts` codebase)
and snapshot content (with latest `go-echarts` release) to distinguish any changes.

Currently, it is WIP and only check the generated content must not be empty. :sweat_smile:

# License

MIT [@Koooooo-7](https://github.com/Koooooo-7)