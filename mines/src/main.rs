use mouse_automation;
use screen_capturer::ScreenCapturer;
use std::collections::HashSet;
use std::{fs::File, io::Write};
// use std::time::Instant;

const XX: &'static [usize] = &[
  205, 255, 305, 355, 405, 455, 505, 553, 603, 653, 703, 753, 803, 853, 903, 953, 1001, 1051, 1101,
  1151, 1201, 1251, 1301, 1351, 1401, 1449, 1499, 1549, 1599, 1649,
];
const YY: &'static [usize] = &[
  313, 363, 413, 463, 513, 561, 611, 661, 711, 761, 811, 861, 911, 961, 1009, 1059,
];

const DX: f32 = 48.13333333333333;
const DY: f32 = 46.625;

const DX_0: usize = ((DX as f32) * 0.2) as usize;
const DY_0: usize = ((DY as f32) * 0.2) as usize;
const DX_1: usize = ((DX as f32) * 0.8) as usize;
const DY_1: usize = ((DY as f32) * 0.8) as usize;

const DS: &'static [f32] = &[
  245.41995074,
  245.42857143,
  245.42857143,
  218.13669951,
  236.22660099,
  240.10344828,
  218.97536946,
  224.2635468,
  205.96305419,
  235.36206897,
  206.18226601,
  217.59605911,
  202.88054187,
  213.17857143,
  232.16133005,
  229.61576355,
  205.40517241,
  205.40517241,
  198.36699507,
  219.54187192,
  203.55172414,
  225.68965517,
  212.87561576,
  225.69458128,
  228.21182266,
  170.71305419,
  64.07758621,
  115.73275862,
  199.08374384,
  255.,
];

const COLOR_MAP: &'static [i32] = &[0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 99];

fn rgb_2_digit(r: f32, g: f32, b: f32) -> i32 {
  let mut min = 10000.0f32;
  let mut ret = 10usize;
  for i in 0..10 {
    let dr = r - DS[i * 3];
    let dg = g - DS[i * 3 + 1];
    let db = b - DS[i * 3 + 2];

    let s = dr * dr + dg * dg + db * db;

    if s < min {
      min = s;
      ret = i;
    }
  }

  return COLOR_MAP[ret];
}

fn deal_screen(screen_capturer: ScreenCapturer) -> [i32; 16 * 30] {
  let mut arr: [i32; 16 * 30] = [0; 16 * 30];

  // let image = screen_capturer.capture().unwrap();

  std::thread::sleep(std::time::Duration::from_millis(500));

  let image = screen_capturer.capture().unwrap();
  println!("=====>");

  // let buffer = image.png().unwrap();
  // let mut file = File::create("debug.png").unwrap();
  // file.write_all(&buffer[..]).unwrap();

  let w = image.width as usize;
  // let h = image.height as usize;
  let data = image.bytes;

  for row in 0..16 {
    for col in 0..30 {
      let mut sum_r: u32 = 0;
      let mut sum_g: u32 = 0;
      let mut sum_b: u32 = 0;
      for y in DY_0..DY_1 {
        for x in DX_0..DX_1 {
          let p = ((YY[row] + y) * w + XX[col] + x) * 4;

          sum_b += data[p] as u32;
          sum_g += data[p + 1] as u32;
          sum_r += data[p + 2] as u32;
        }
      }

      let cnt = ((DY_1 - DY_0) * (DX_1 - DX_0)) as f32;
      let avg_r = sum_r as f32 / cnt;
      let avg_g = sum_g as f32 / cnt;
      let avg_b = sum_b as f32 / cnt;

      arr[30 * row + col] = rgb_2_digit(avg_r, avg_g, avg_b);
    }
  }

  return arr;
}

struct Global {
  g_2: HashSet<usize>,
}

fn around_count(g: &mut Global, mat: &[i32], row_u: usize, col_u: usize) -> i32 {
  let mut ret = 0;
  let mut f_cnt = 0;

  let row_col = row_u * 30 + col_u;
  let row = row_u as isize;
  let col = col_u as isize;

  for ddy in -1..2 {
    for ddx in -1..2 {
      let y = row + ddy;
      let x = col + ddx;

      if x >= 0 && x < 30 && y >= 0 && y < 16 {
        let v = mat[(y * 30 + x) as usize];
        if v > 8 {
          ret += 1;
        }
        if v == 9 {
          f_cnt += 1;
        }
      }
    }
  }

  if ret == f_cnt {
    if mat[row_col] == f_cnt {
      g.g_2.insert(row_col);
    }
  }
  return ret;
}

fn flag_around(mat: &mut [i32], row_u: usize, col_u: usize) -> i32 {
  let mut ret = 0;

  let row_col = row_u * 30 + col_u;
  let row = row_u as isize;
  let col = col_u as isize;

  for ddy in -1..2 {
    for ddx in -1..2 {
      let y = row + ddy;
      let x = col + ddx;

      if x >= 0 && x < 30 && y >= 0 && y < 16 {
        let v = mat[(y * 30 + x) as usize];
        if v == 11 {
          ret += 1;
          right_c(mat, x as usize, y as usize);
        }
      }
    }
  }

  return ret;
}

fn flag_count(mat: &[i32], row_u: usize, col_u: usize) -> (i32, i32) {
  let mut flag_cnt = 0;
  let mut unknown_cnt = 0;

  let row_col = row_u * 30 + col_u;
  let row = row_u as isize;
  let col = col_u as isize;

  for ddy in -1..2 {
    for ddx in -1..2 {
      let y = row + ddy;
      let x = col + ddx;

      if x >= 0 && x < 30 && y >= 0 && y < 16 {
        let v = mat[(y * 30 + x) as usize];

        if v == 9 {
          flag_cnt += 1;
        } else if v == 11 {
          unknown_cnt += 1;
        }
      }
    }
  }

  return (flag_cnt, unknown_cnt);
}

fn s1(g: &mut Global, mat: &mut [i32]) -> i32 {
  let mut ret = 0;
  println!("s1");

  for row in 0..16usize {
    for col in 0..30 {
      let row_col = row * 30 + col;
      if g.g_2.contains(&row_col) {
        continue;
      }

      let v = mat[row_col];
      if v > 0 && v < 9 {
        if around_count(g, mat, row, col) == v {
          ret += flag_around(mat, row, col);
        }
      } else if v == 0 {
        g.g_2.insert(row_col);
      }
    }
  }
  return ret;
}

fn s2(g: &Global, mat: &[i32]) -> i32 {
  let mut ret = 0;
  println!("s2");

  for row in 0..16 {
    for col in 0..30 {
      let row_col = row * 30 + col;
      if g.g_2.contains(&row_col) {
        continue;
      }

      let v = mat[row_col];
      if v > 0 && v < 9 {
        let (flag_cnt, unkown_cnt) = flag_count(mat, row, col);
        if v == flag_cnt && unkown_cnt > 0 {
          ret += 1;
          middle_c(mat, col, row)
        }
      }
    }
  }

  return ret;
}

fn around_set_ex(mat: &[i32], row_u: usize, col_u: usize) -> (HashSet<usize>, HashSet<usize>) {
  let mut un_set = HashSet::new();
  let mut f_set = HashSet::new();

  // let row_col = row_u * 30 + col_u;
  let row = row_u as isize;
  let col = col_u as isize;

  for ddy in -1..2 {
    for ddx in -1..2 {
      let y = row + ddy;
      let x = col + ddx;

      if x >= 0 && x < 30 && y >= 0 && y < 16 {
        let v = mat[(y * 30 + x) as usize];

        if v == 9 {
          f_set.insert((y * 256 + x) as usize);
        } else if v == 11 {
          un_set.insert((y * 256 + x) as usize);
        }
      }
    }
  }

  return (un_set, f_set);
}

fn sub_4(mat: &mut [i32], row_u: usize, col_u: usize) -> i32 {
  let mut ret = 0;

  let row_col = row_u * 30 + col_u;
  let row = row_u as isize;
  let col = col_u as isize;

  let v = mat[row_col];
  if v > 0 && v < 9 {
    let (my_set, f_my_set) = around_set_ex(mat, row_u, col_u);
    let my_un = v - f_my_set.len() as i32;
    if my_set.len() > 0 {
      for ddy in -2..3 {
        for ddx in -2..3 {
          let y = ddy + row;
          let x = ddx + col;
          if x >= 0 && x < 30 && y >= 0 && y < 16 {
            let v_2 = mat[(y * 30 + x) as usize];
            if v_2 > 0 && v_2 < 9 {
              let (un_set_2, f_set_2) = around_set_ex(mat, y as usize, x as usize);
              let un_2 = v_2 - f_set_2.len() as i32;
              if my_set.is_subset(&un_set_2) && !un_set_2.is_subset(&my_set) {
                let a: Vec<&usize> = un_set_2.difference(&my_set).collect();
                if my_un == un_2 {
                  for aa in &a {
                    let y_2 = *aa / 256;
                    let x_2 = *aa % 256;
                    left_c(mat, x_2, y_2);
                    ret += 1;
                  }
                }
                if un_2 - my_un == (a.len() as i32) {
                  for aa in &a {
                    let y_2 = *aa / 256;
                    let x_2 = *aa % 256;
                    right_c(mat, x_2, y_2);
                    ret += 1;
                  }
                }
              }
              if ret > 0 {
                return ret;
              }

              let a: Vec<&usize> = un_set_2.difference(&my_set).collect();
              if un_2 - my_un == (a.len() as i32) {
                for aa in &a {
                  let y_2 = *aa / 256;
                  let x_2 = *aa % 256;
                  right_c(mat, x_2, y_2);
                  ret += 1;
                }
              }
            }
          }
        }
      }
    }
  }

  return ret;
}

fn s4(mat: &mut [i32]) -> i32 {
  let mut ret = 0;

  for row in 0..16 {
    for col in 0..30 {
      let v = mat[row * 30 + col];
      if v > 0 && v < 9 {
        ret += sub_4(mat, row, col);
      }
    }
  }
  return ret;
}

fn do2(g: &mut Global, screen_capturer: ScreenCapturer) {
  loop {
    loop {
      let mut n = 0;
      let mut a = deal_screen(screen_capturer);
      n += s1(g, &mut a);
      n += s2(g, &mut a);
      if n == 0 {
        println!("b12");
        break;
      }
    }
    let mut a = deal_screen(screen_capturer);
    let n4 = s4(&mut a);
    if n4 > 0 {
      continue;
    } else {
      break;
    }
  }
}

fn init(g: &mut Global) {
  g.g_2 = HashSet::new();
}

fn start(g: &mut Global, screen_capturer: ScreenCapturer) {
  loop {
    let mut line = String::new();
    let _ = std::io::stdin().read_line(&mut line);
    println!("Got input");
    init(g);
    do2(g, screen_capturer);
    mouse_automation::move_mouse(400/2, 200/2, true);
  }
}

static MOVE_LAG:u64 = 300;
static CLICK_LAG:u64 = 100;

fn right_c(mat: &mut [i32], x: usize, y: usize) {
  // println!(
  //   "right_c x {} y {}",
  //   (XX[x] + ((DX / 2.0) as usize)) as i32,
  //   (YY[y] + ((DY / 2.0) as usize)) as i32
  // );
  mouse_automation::move_mouse(
    ((XX[x] + ((DX / 2.0) as usize)) / 2) as i32,
    ((YY[y] + ((DY / 2.0) as usize)) / 2) as i32,
    true,
  );
  std::thread::sleep(std::time::Duration::from_millis(MOVE_LAG));

  mouse_automation::RIGHT.down();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
  mouse_automation::RIGHT.up();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
  mat[y * 30 + x] = 9;
}

fn left_c(_mat: &[i32], x: usize, y: usize) {
  mouse_automation::move_mouse(
    ((XX[x] + ((DX / 2.0) as usize)) / 2) as i32,
    ((YY[y] + ((DY / 2.0) as usize)) / 2) as i32,
    true,
  );
  std::thread::sleep(std::time::Duration::from_millis(MOVE_LAG));

  mouse_automation::LEFT.down();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
  mouse_automation::LEFT.up();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
}

fn middle_c(_mat: &[i32], x: usize, y: usize) {
  mouse_automation::move_mouse(
    ((XX[x] + ((DX / 2.0) as usize)) / 2) as i32,
    ((YY[y] + ((DY / 2.0) as usize)) / 2) as i32,
    true,
  );
  std::thread::sleep(std::time::Duration::from_millis(MOVE_LAG));

  mouse_automation::MIDDLE.down();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
  mouse_automation::MIDDLE.up();
  std::thread::sleep(std::time::Duration::from_millis(CLICK_LAG));
}

fn main() {
  // let start = Instant::now();

  // let screen_capturers = ScreenCapturer::all();

  // for screen_capturer in screen_capturers {
  //   println!("capturer {:?}", screen_capturer);
  //   let image = screen_capturer.capture().unwrap();
  //   // let buffer = image.png().unwrap();
  //   // let display_id = screen_capturer.display_info.id.to_string();
  //   // let path = String::from("") + &display_id + ".png";
  //   // let mut file = File::create(path).unwrap();
  //   // file.write_all(&buffer[..]).unwrap();
  // }

  let screen_capturer = ScreenCapturer::from_point(100, 100).unwrap();
  // println!("capturer {:?}", screen_capturer);

  // let image = screen_capturer.capture().unwrap();
  // let buffer = image.png().unwrap();
  // let mut file = File::create("capture_display_with_point.png").unwrap();
  // file.write_all(&buffer[..]).unwrap();

  // println!("运行耗时: {:?}", start.elapsed());

  mouse_automation::move_mouse(1400 / 2, 800 / 2, true);

  // let mut a = deal_screen(screen_capturer);

  let mut g = Global {
    g_2: HashSet::new(),
  };

  // s1(&mut g, &mut a);

  if true {
    start(&mut g, screen_capturer);
  }

  println!("Done");
}
