local M = {}

---@class plug_opts
---@field local_path string|function?
---@field save "local_file"|"local"|"online"
---@field filename string|function?
---@field default_ft string

---@class config
---@field opts plug_opts
---@field ft table<string, string>

---@type config
M.config = {
	opts = {
		local_path = '/assets/imgs/',
		save = 'local',
		filename = '',
		default_ft = 'markdown',
	},
	ft = {
		markdown = '![]($IMG$)',
		vimwiki = '{{file:$IMG$}}',
	},
}

local imagePathRule
local fileNameRule

M.getConfig = function()
	imagePathRule = M.config.opts.local_path
	fileNameRule = M.config.opts.filename
	M.config.opts.local_path = nil
	M.config.opts.filename = nil
	return M.config
end

M.getFileName = function()
	if type(fileNameRule) == 'function' then
		return fileNameRule()
	end
	return fileNameRule
end

M.getFilePath = function()
	local file = vim.api.nvim_buf_get_name(vim.api.nvim_get_current_buf())
	return file:match("(.*[/\\])")
end

M.createImagePathName = function()
	if type(imagePathRule) == 'function' then
		return imagePathRule()
	end
	return imagePathRule
end

local function create_command()
	if not vim.fn.exists 'python3' then
		print 'Make sure python3 is installed for pastify.nvim to work.'
		return
	end

	vim.cmd [[
    python3 import pastify.main
    python3 image = pastify.main.Pastify()

    command! -range Pastify python3 image.paste_text(0)
    command! -range PastifyAfter python3 image.paste_text(1)
  ]]
end

---@param params config
M.setup = function(params)
	M.config = vim.tbl_deep_extend('force', {}, M.config, params)
	create_command()
end

return M
