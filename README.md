# pastify.nvim

A fork of ["gmohlamo/pastify.nvim"](https://github.com/gmohlamo/pastify.nvim), but I just made minor changes for use with VimWiki.
The main difference is that I removed the upload functionality and made all paste efforts create a time stamped image relative to the note that you are pasting it into.

## Requirements

- Neovim 0.8+
- MacOS or Windows (No extra tools needed)
- Linux (with `xclip` or `wl-paste` installed)
- Python3
- Pip3

## Installation

Make sure Neovim has python3 by running `:checkhealth`, if you have python but it is not linked, run `pip3 install neovim`.
Then, run `pip3 install pillow`.

```lua
return {
  'gmohlamo/pastify.nvim',
  cmd = { 'Pastify', 'PastifyAfter' },
  config = function()
    require('pastify').setup {
      opts = {
        apikey = "YOUR API KEY (https://api.imgbb.com/)", -- Needed if you want to save online.
      },
    }
  end
}
```

## Configuration

These are the default options, you don't need to copy them into `setup()`

```lua
require('pastify').setup {
  opts = {
    absolute_path = false, -- use absolute or relative path to the working directory
    apikey = '', -- Api key, required for online saving
    local_path = '/assets/imgs/', -- The path to put local files in, ex <cwd>/assets/images/<filename>.png
    save = 'local', -- Either 'local' or 'online' or 'local_file'
    filename = '', -- The file name to save the image as, if empty pastify will ask for a name
    -- Example function for the file name that I like to use:
    -- filename = function() return vim.fn.expand("%:t:r") .. '_' .. os.date("%Y-%m-%d_%H-%M-%S") end,
    -- Example result: 'file_2021-08-01_12-00-00'
    default_ft = 'markdown', -- Default filetype to use
  },
  ft = { -- Custom snippets for different filetypes, will replace $IMG$ with the image url
    vimwiki = '{{file:$IMG$}}',
    markdown = '![]($IMG$)',
  },
}
```

#### Options

**aboslute_path** - If true, the path will be absolute, if false, the path will be relative to either the current file or current working directory (depending on the **save** option).

**local_path** - The path to save local files in, relative to the current working directory. This can be a lua function. I'll probably be removing this too...

**save** - Either 'local' or 'online' or 'local_file'. 'local' will save the image locally relative to the current working directory, 'online' will save the image online, 'local_file' will save the image locally relative to the file path. This is also gonna leave...

**default_ft** - The default filetype to use if the filetype is not in the **ft** table. I'll be removing this in an effort to clean up the codebase.

#### File Types

Each filetype can have a custom snippet that will replace `$IMG$` with the image url. This can be useful for markdown, html, or latex.

### Custom Keybinding

I like to add a custom binding to paste from my system clipboard that doesn't specifically rely on image or text, it simply pastes whatever is in the clipboard.

```lua
vim.api.nvim_set_keymap('v', '<leader>p', ':PastifyAfter<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>p', ':PastifyAfter<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>P', ':Pastify<CR>', { noremap = true, silent = true })
```

Or if you prefer to do everything in lazy.nvim, here is my config:

```lua
return {
    'gmohlamo/pastify.nvim',
    cmd = { 'Pastify', 'PastifyAfter' },
    event = { 'BufReadPost' }, -- Load after the buffer is read, I like to be able to paste right away
    keys = {
        {noremap = true, mode = "x", '<leader>p', "<cmd>PastifyAfter<CR>"},
        {noremap = true, mode = "n", '<leader>p', "<cmd>PastifyAfter<CR>"},
        {noremap = true, mode = "n", '<leader>P', "<cmd>Pastify<CR>"},
    },
    config = function()
        require('pastify').setup({
            opts = {
                absolute_path = false, -- use absolute or relative path to the working directory
                apikey = '', -- Api key, required for online saving
                local_path = '/assets/imgs/', -- The path to put local files in, ex ~/Projects/<name>/assets/images/<imgname>.png
                save = 'local', -- To be deprecated
                default_ft = 'markdown', -- Default filetype to use
            },
            ft = { -- Custom snippets for different filetypes, will replace $IMG$ with the image url
                vimwiki = '{{file:$IMG$}}',
                markdown = '![]($IMG$)',
            },
        })
    end
}
```
