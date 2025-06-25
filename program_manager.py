import os
import subprocess
import threading
import time
import psutil
import tempfile

class ProgramManager:
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        self.programs = {}  # {program_id: {'path': path, 'name': name, 'process': process, 'position': (x,y), 'status': status}}
        self.next_program_id = 1
        self.batch_files = {}  # {program_id: batch_file_path} - 배치 파일 경로 추적
    
    def run_program(self, program_path, params, position_name):
        """Run program using hidden batch file"""
        if not os.path.exists(program_path):
            self.logger.log(self.config_manager.get_message('errors.program_not_found', path=program_path))
            return None
        
        x, y = self.config_manager.get_position_coords(position_name)
        
        program_id = self.next_program_id
        self.next_program_id += 1
        
        self.logger.log(self.config_manager.get_message('program_execution_start', id=program_id))
        self.logger.log(self.config_manager.get_message('program_name', name=os.path.basename(program_path)))
        self.logger.log(self.config_manager.get_message('position_set', position=self.config_manager.get_position_name((x, y))))
        
        try:
            program_dir = os.path.dirname(program_path)
            program_name = os.path.basename(program_path)
            process_name = os.path.splitext(program_name)[0]
            
            # Create completely hidden batch file
            batch_content = f"""@echo off
cd /d "{program_dir}"
start "" "{program_name}" {params}
"""
            
            # 임시 디렉토리에 숨겨진 배치 파일 생성
            temp_dir = tempfile.gettempdir()
            temp_bat = os.path.join(temp_dir, f"temp_program_{program_id}.bat")
            
            with open(temp_bat, "w", encoding="cp949") as f:
                f.write(batch_content)
            
            # 배치 파일을 숨김 속성으로 설정
            try:
                import win32file
                win32file.SetFileAttributes(temp_bat, win32file.FILE_ATTRIBUTE_HIDDEN)
            except ImportError:
                pass
            
            # 배치 파일을 완전히 숨겨진 상태로 실행
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # cmd /c를 사용하여 배치 파일을 숨겨진 상태로 실행
            process = subprocess.Popen(['cmd', '/c', temp_bat], 
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     startupinfo=startupinfo,
                                     creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
            
            # 배치 파일 경로 저장
            self.batch_files[program_id] = temp_bat
            
            # Save program information
            self.programs[program_id] = {
                'path': program_path,
                'name': program_name,
                'process_name': process_name,
                'position': (x, y),
                'status': 'Running',
                'pid': None
            }
            
            # Start auto position adjustment
            self.auto_adjust_position(program_id)
            
            return program_id
            
        except Exception as e:
            self.logger.log(self.config_manager.get_message('errors.program_execution_error', id=program_id, error=str(e)))
            return None
    
    def cleanup_batch_file(self, program_id):
        """배치 파일 정리"""
        if program_id in self.batch_files:
            batch_file = self.batch_files[program_id]
            try:
                if os.path.exists(batch_file):
                    os.remove(batch_file)
                    self.logger.log(f"배치 파일 삭제됨: {batch_file}")
            except Exception as e:
                self.logger.log(f"배치 파일 삭제 실패: {e}")
            finally:
                del self.batch_files[program_id]
    
    def auto_adjust_position(self, program_id):
        """Auto position adjustment using PowerShell (wait in Python)"""
        def auto_adjust():
            if program_id not in self.programs:
                return
            
            program_info = self.programs[program_id]
            x, y = program_info['position']
            process_name = program_info['process_name']
            
            self.logger.log(self.config_manager.get_message('auto_position_start', id=program_id))
            
            # Maximum attempts
            max_attempts = self.config_manager.config['monitoring']['max_position_attempts']
            attempt_interval = self.config_manager.config['monitoring']['position_attempt_interval']
            timeout = self.config_manager.config['monitoring']['timeout']
            
            # 파이썬에서 대기 (2초)
            time.sleep(2)
            
            for attempt in range(1, max_attempts + 1):
                try:
                    tracked_pids = [info.get('pid') for info in self.programs.values() if info.get('pid')]
                    pid = self._adjust_position_powershell(program_info, x, y, tracked_pids)
                    if pid:
                        self.programs[program_id]['pid'] = pid
                        self.programs[program_id]['status'] = 'Running'
                        self.logger.log(self.config_manager.get_message('position_adjust_success', id=program_id, pid=pid))
                        return
                    else:
                        self.logger.log(self.config_manager.get_message('progress.waiting_for_process', id=program_id, attempt=attempt))
                    time.sleep(attempt_interval)
                except Exception as e:
                    self.logger.log(self.config_manager.get_message('progress.attempt_error', id=program_id, attempt=attempt, error=str(e)))
                    time.sleep(attempt_interval)
            self.logger.log(self.config_manager.get_message('position_adjust_failed', id=program_id))
        thread = threading.Thread(target=auto_adjust, daemon=True)
        thread.start()
    
    def _adjust_position_powershell(self, program_info, x, y, tracked_pids):
        """PowerShell을 사용한 위치 조정"""
        try:
            process_name = program_info['process_name']
            timeout = self.config_manager.config['monitoring']['timeout']
            if program_info.get('pid'):
                ps_script = f"""
                try {{
                    $proc = Get-Process -Id {program_info['pid']} -ErrorAction Stop
                    if ($proc.MainWindowHandle -ne [IntPtr]::Zero) {{
                        Add-Type -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);' -Name 'WinApi' -Namespace 'User32'
                        $hwnd = $proc.MainWindowHandle
                        $result = [User32.WinApi]::SetWindowPos($hwnd, 0, {x}, {y}, 640, 480, 0x0000)
                        if ($result) {{
                            Write-Host \"성공\"
                            Write-Host $proc.Id
                        }} else {{
                            Write-Host \"실패\"
                        }}
                    }} else {{
                        Write-Host \"창 없음\"
                    }}
                }} catch {{
                    Write-Host \"프로세스 없음\"
                }}
                """
            else:
                ps_script = f"""
                $processName = '{process_name}'
                $processes = Get-Process -Name $processName -ErrorAction SilentlyContinue
                if ($processes) {{
                    $trackedPids = @({', '.join([str(pid) for pid in tracked_pids])})
                    foreach ($proc in $processes) {{
                        if ($proc.Id -notin $trackedPids -and $proc.MainWindowHandle -ne [IntPtr]::Zero) {{
                            Add-Type -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);' -Name 'WinApi' -Namespace 'User32'
                            $hwnd = $proc.MainWindowHandle
                            $result = [User32.WinApi]::SetWindowPos($hwnd, 0, {x}, {y}, 640, 480, 0x0000)
                            if ($result) {{
                                Write-Host \"성공\"
                                Write-Host $proc.Id
                            }} else {{
                                Write-Host \"실패\"
                            }}
                            break
                        }}
                    }}
                }} else {{
                    Write-Host \"프로세스 없음\"
                }}
                """
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(['powershell', '-Command', ps_script], 
                                  capture_output=True, text=True, timeout=timeout,
                                  startupinfo=startupinfo,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            if "성공" in result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    return int(lines[1])
            return None
        except Exception as e:
            self.logger.log(f"PowerShell position adjustment error: {e}")
            return None
    
    def adjust_program_position(self, program_id, x, y):
        """Adjust position of specific program using PowerShell"""
        def adjust():
            if program_id not in self.programs:
                return
            program_info = self.programs[program_id]
            process_name = program_info['process_name']
            try:
                tracked_pids = [info.get('pid') for info in self.programs.values() if info.get('pid')]
                pid = self._adjust_position_powershell(program_info, x, y, tracked_pids)
                if pid:
                    self.logger.log(self.config_manager.get_message('position_adjust_manual_success', id=program_id))
                else:
                    self.logger.log(self.config_manager.get_message('warnings.process_not_found', id=program_id))
            except Exception as e:
                self.logger.log(self.config_manager.get_message('errors.position_adjust_error', id=program_id, error=str(e)))
        thread = threading.Thread(target=adjust, daemon=True)
        thread.start()
    
    def terminate_program(self, program_id):
        """Terminate specific program"""
        if program_id not in self.programs:
            self.logger.log(self.config_manager.get_message('errors.program_info_not_found', id=program_id))
            return
        program_info = self.programs[program_id]
        process_name = program_info['process_name']
        self.logger.log(self.config_manager.get_message('progress.program_terminating', id=program_id))
        try:
            if program_info.get('pid'):
                try:
                    proc = psutil.Process(program_info['pid'])
                    proc.terminate()
                    self.logger.log(self.config_manager.get_message('program_terminated', id=program_id, pid=program_info['pid']))
                except psutil.NoSuchProcess:
                    self.logger.log(self.config_manager.get_message('warnings.process_already_terminated', id=program_id, pid=program_info['pid']))
                except Exception as e:
                    self.logger.log(self.config_manager.get_message('errors.terminate_error', id=program_id, error=str(e)))
            else:
                tracked_pids = [info.get('pid') for info in self.programs.values() if info.get('pid')]
                for proc in psutil.process_iter(['pid', 'name']):
                    if (proc.info['name'] and 
                        proc.info['name'].lower() == f"{process_name}.exe".lower() and
                        proc.info['pid'] not in tracked_pids):
                        proc.terminate()
                        self.logger.log(self.config_manager.get_message('program_terminated', id=program_id, pid=proc.info['pid']))
                        break
                else:
                    self.logger.log(self.config_manager.get_message('warnings.process_not_found', id=program_id))
            
            # Clean up batch file
            self.cleanup_batch_file(program_id)
            
            del self.programs[program_id]
        except Exception as e:
            self.logger.log(self.config_manager.get_message('errors.terminate_error', id=program_id, error=str(e)))
    
    def terminate_all_programs(self):
        """Terminate all programs"""
        self.logger.log(self.config_manager.get_message('progress.all_programs_terminating'))
        program_ids = list(self.programs.keys())
        for program_id in program_ids:
            self.terminate_program(program_id)
        
        # Clean up any remaining batch files
        for program_id in list(self.batch_files.keys()):
            self.cleanup_batch_file(program_id)
        
        self.logger.log(self.config_manager.get_message('all_programs_terminated'))
    
    def update_program_position(self, program_id, position_name):
        """Update program position information"""
        if program_id in self.programs:
            x, y = self.config_manager.get_position_coords(position_name)
            self.programs[program_id]['position'] = (x, y)
            return True
        return False
    
    def get_programs(self):
        """Get all programs"""
        return self.programs
    
    def get_program(self, program_id):
        """Get specific program"""
        return self.programs.get(program_id)
    
    def check_program_status(self, program_id):
        """Check if program is still running"""
        if program_id not in self.programs:
            return False
        program_info = self.programs[program_id]
        if program_info.get('pid'):
            try:
                proc = psutil.Process(program_info['pid'])
                if not proc.is_running():
                    self.logger.log(self.config_manager.get_message('program_closed', id=program_id))
                    # Clean up batch file when program closes
                    self.cleanup_batch_file(program_id)
                    del self.programs[program_id]
                    return False
            except psutil.NoSuchProcess:
                self.logger.log(self.config_manager.get_message('program_closed', id=program_id))
                # Clean up batch file when program closes
                self.cleanup_batch_file(program_id)
                del self.programs[program_id]
                return False
        return True 